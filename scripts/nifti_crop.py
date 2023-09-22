import nibabel as nib
import numpy as np

import sys
import os

if len(sys.argv) != 2:
    print("Usage: python nifti_crop.py <imageToCrop>")
    sys.exit(1)

imageToCrop = sys.argv[1]

# Now you can use filename_without_extension in your Python script
print("Nifti Image:", imageToCrop)

# Load the NIfTI image
image_path = imageToCrop  # Replace with your image path in quotations marks if not in the same directory
img = nib.load(image_path)

# Get the NIfTI image data as a NumPy array
img_data = img.get_fdata()

# Define the cropping coordinates (xmin, xmax, ymin, ymax, zmin, zmax)
# Replace these values with the desired cropping range
xmin, xmax = 6, 173  # Crop in the x-axis from voxel 6 to 173
ymin, ymax = 2, 214  # Crop in the y-axis from voxel 2 to 214
zmin, zmax = 0, 160  # Crop in the z-axis from voxel 0 to 160

# Crop the image data
cropped_data = img_data[xmin:xmax, ymin:ymax, zmin:zmax]

# Create a new NIfTI image with the cropped data
cropped_img = nib.Nifti1Image(cropped_data, img.affine)

outImage_wo_gz = os.path.splitext(imageToCrop)[0]
outImage = os.path.splitext(outImage_wo_gz)[0]

# Save the cropped NIfTI image to a new file
output_path = outImage + "_crop.nii.gz"  # Replace with your output path if different
nib.save(cropped_img, output_path)

print(f"Cropped image saved to {output_path}")
exit()