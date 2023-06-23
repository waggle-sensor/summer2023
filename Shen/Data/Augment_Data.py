import os
from PIL import Image

def rotate_images(directory, rotation_angle):
    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"{directory} does not exist.")
        return

    # Loop over every file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            # Open image
            img_path = os.path.join(directory, filename)
            img = Image.open(img_path)
            
            # Create rotated image
            rotated_img = img.rotate(rotation_angle)

            # Save rotated image
            new_filename = os.path.splitext(filename)[0] + '_rotated' + os.path.splitext(filename)[1]
            new_img_path = os.path.join(directory, new_filename)
            rotated_img.save(new_img_path)

# Use the function

# for x in ['0-200', '200-400','400-600','600-800','800-1000']:
#     rotate_images(f'/Users/alexshen/desktop/BaseDir2_augment/train/{x}', 90)


