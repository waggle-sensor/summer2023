import os
import shutil

source_dir = '/Users/alexshen/desktop/BaseDir2_augment/train/800-1000'
dest_dir = '/Users/alexshen/desktop/BaseDir2_augment/val/800-1000'

# Get all files in the source directory
files = os.listdir(source_dir)

# Filter out files to get images (assuming .jpg format here)
images = [file for file in files if file.endswith('.jpg')]

# Iterate over the images, moving every 10th one
for i, img in enumerate(images, start=1):
    if i % 9 == 0:  
        src_path = os.path.join(source_dir, img)
        dest_path = os.path.join(dest_dir, img)
        shutil.move(src_path, dest_path)  
