import os
import sys
import nibabel as nib
import numpy as np

def crop_nifti(input_path, output_path):
    # Load the NIfTI image
    img = nib.load(input_path)

    # Get the NIfTI image data as a NumPy array
    img_data = img.get_fdata()

    # Define the cropping coordinates (xmin, xmax, ymin, ymax, zmin, zmax)
    # Replace these values with the desired cropping range if different
    xmin, xmax = 6, 173  # Crop in the x-axis from voxel 6 to 173
    ymin, ymax = 2, 214  # Example: Crop in the y-axis from voxel 2 to 214
    zmin, zmax = 0, 160  # Example: Crop in the z-axis from voxel 0 to 160

    # Crop the image data
    cropped_data = img_data[xmin:xmax, ymin:ymax, zmin:zmax]

    # Create a new NIfTI image with the cropped data
    cropped_img = nib.Nifti1Image(cropped_data, img.affine)

    # Save the cropped NIfTI image to a new file
    nib.save(cropped_img, output_path)

    print(f"Cropped image saved to {output_path}")

def main():
    # Check the number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python nifti_crop_batch.py /path/to/input_directory /path/to/output_directory")
        sys.exit(1)

    # Get the input and output directories from command-line arguments
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    # List all files in the input directory
    input_files = [f for f in os.listdir(input_directory) if f.endswith('.nii.gz')]

    # Iterate over each input file
    for input_file in input_files:
        # Construct the full path for the input file
        input_path = os.path.join(input_directory, input_file)

        # Generate the output file name
        output_file = input_file.replace('.nii.gz', '_crop.nii.gz')

        # Construct the full path for the output file
        output_path = os.path.join(output_directory, output_file)

        # Call the crop function
        crop_nifti(input_path, output_path)

    print("Processing complete.")

if __name__ == "__main__":
    main()