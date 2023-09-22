Repository containing code, models and tutorials for the paper [Deep neural networks learn general and clinically relevant representations of the ageing brain](https://www.medrxiv.org/content/10.1101/2021.10.29.21265645v1)

# Installation (via terminal and Anaconda)

1. Clone the github repo<br />
```git clone git@github.com:estenhl/pyment-public.git```
2. Enter the folder<br />
```cd pyment-public```
3. Create a conda environment<br />
```conda create --name pyment python=3.9```
4. Activate environment<br />
```conda activate pyment```
5. Install required packages<br />
```pip install -r requirements.txt```
6. Install Tensorflow<br />
a. Tensorflow for GPU<br />
```pip install tensorflow-gpu```<br />
b. Tensorflow for CPU<br />
```pip install tensorflow```
6. Source the package<br />
```conda develop .```

# Preparing data
While the models adhere to the Keras [Model](https://www.tensorflow.org/api_docs/python/tf/keras/Model) interface and can thus be used however one wants, we have provided [Dataset](https://github.com/estenhl/pyment-public/blob/main/pyment/data/datasets/nifti_dataset.py)/[Generator](https://github.com/estenhl/pyment-public/blob/main/pyment/data/generators/async_nifti_generator.py)-classes for nifti-files which are used in the tutorials. For these classes to work off-the-shelf the Nifti-data has to be organized in the following folder structure:
```
.
├── labels.csv
└── images
      ├── image1.nii.gz
      ├── image2.nii.gz
     ...
      └── imageN.nii.gz
``` 
where ```labels.csv``` is a csv-file with column ```id``` (corresponding to image1, image2, etc) and column ```age```.

## Preprocessing
Before training the models all images were ran through the following preprocessing pipeline:

1. Extract brainmask with ```recon-all -s {ID} -i {T1} -o {ID} -all``` (FreeSurfer) #Can instead run --autorecon1
2. Transform to *.nii.gz with ```mri_convert $SUBJECTS_DIR/{ID}/mri/brain.mgz /tmp_processing_dir/{ID}_brain.nii.gz``` (FreeSurfer)
3. Translate to FSL space with ```fslreorient2std /tmp_processing_dir/{ID}_brain.nii.gz /tmp_processing_dir/{ID}_brain2std.nii.gz``` (FSL)
4. Register to MNI space with ```flirt -in /tmp_processing_dir/{ID}_brain2std.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz -out /tmp_processing_dir/{ID}_brain2mni.nii.gz -omat /tmp_processing_dir/{ID}_brain2mni.mat -dof 6``` (FSL, rigid body registration), and the standard FSL template ```MNI152_T1_1mm_brain.nii.gz```
5. Crop away borders of ```[6:173,2:214,0:160]```

To crop borders, you can use the following code (Python script also available in scripts: nifti_crop.py):

```#In a Bash terminal
pip install nibabel
cd /directory/where/images/to/crop/are
python

#Within Python
import nibabel as nib
import numpy as np

# Load the NIfTI image
image_path = "your_mri_image.nii.gz"  # Replace with your image path
img = nib.load(image_path)

# Get the NIfTI image data as a NumPy array
img_data = img.get_fdata()

# Define the cropping coordinates (xmin, xmax, ymin, ymax, zmin, zmax)
# Replace these values with the desired cropping range
xmin, xmax = 6, 173  # Example: Crop in the x-axis from voxel 10 to 90
ymin, ymax = 2, 214  # Example: Crop in the y-axis from voxel 20 to 120
zmin, zmax = 0, 160  # Example: Crop in the z-axis from voxel 0 to 80

# Crop the image data
cropped_data = img_data[xmin:xmax, ymin:ymax, zmin:zmax]

# Create a new NIfTI image with the cropped data
cropped_img = nib.Nifti1Image(cropped_data, img.affine)

# Save the cropped NIfTI image to a new file
output_path = "cropped_mri_image.nii.gz"  # Replace with your output path
nib.save(cropped_img, output_path)

print(f"Cropped image saved to {output_path}")
exit()
```
A full example which downloads the IXI dataset and preprocesses it can be found in the [Preprocessing tutorial](https://github.com/estenhl/pyment-public/blob/main/notebooks/Download%20and%20preprocess%20IXI.ipynb)

# Estimating brain age in Python
Estimating brain age using the trained brain age model from the paper consists of downloading the weights, instantiating the model with said weights, and calling [Model.fit()](https://www.tensorflow.org/api_docs/python/tf/keras/Model#predict) with an appropriate generator.

#If needed, build the Singularity container
```
singularity build pyment.sif docker://estenhl/sfcn-reg-predict-brain-age
```
#Run the prediction in Singularity
```
singularity run \
  --cleanenv \
  --bind /path/to/preprocessed_images:/images \
  --bind /path/to/pyment_predictions:/predictions \
  pyment.sif
```
#Run the prediction in Docker
```
docker run \
      --rm \
      --name predict-brain-age \
      --mount type=bind,source=/path/to/preprocessed_images,target=/images \
      --mount type=bind,source=/path/to/pyment_predictions,target=/predictions \
      estenhl/sfcn-reg-predict-brain-age
```

A full tutorial (which relies on having a prepared dataset) can be found in the [Python prediction tutorial](https://github.com/estenhl/pyment-public/blob/main/notebooks/Encode%20dataset%20as%20feature%20vectors.ipynb)

Instructions for downloading, building and using our docker containers for brain age predictions can be found in the [docker](https://github.com/estenhl/pyment-public/tree/main/docker)-folder
