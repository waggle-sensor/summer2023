import os
from PIL import Image, ImageDraw, ImageOps

def circle_crop_image(input_path, output_path):
    # Open image and ensure it is RGB
    img = Image.open(input_path).convert("RGB")

    # Create mask
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)

    # Apply mask to image
    result = img.copy()
    result.putalpha(mask)

    # Find bounding box
    bbox = ImageOps.invert(mask).getbbox()

    # Crop the image to the bounding box
    result = result.crop(bbox)

    # Save the image to output_path
    result.save(output_path, "PNG")

def circle_crop_all_in_dir(input_dir, output_dir):
    # Get a list of all image file names in the directory
    file_names = os.listdir(input_dir)
    
    # Loop through all files
    for file_name in file_names:
        if file_name.endswith('.jpg'):
            # Generate full file path
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            
            # Apply circular crop to image and save to new directory
            circle_crop_image(input_path, output_path)

# Use the function like this:
list = ['0-100', '100-200', '200-300', '300-400', '400-500', '500-600', '600-700', '700-800', '800-900', '900-1000']
for i in list:
    circle_crop_all_in_dir(f"/Users/alexshen/Desktop/BaseDir_augment_original/train/{i}", f"/Users/alexshen/Desktop/BaseDir_augment_circles/train/{i}")
