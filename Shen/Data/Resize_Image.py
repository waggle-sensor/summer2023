import cv2
import os

# specify your path
path = '/Users/alexshen/desktop/Test_Im'

# use os.listdir to get all files in the directory
image_files = os.listdir(path)

# loop through each file
for image_file in image_files:
    # check if the file is an image
    if image_file.endswith(('.jpg')):
        # join the folder path and files
        full_path = os.path.join(path, image_file)
        
        # read the image
        image = cv2.imread(full_path)
        
        # resize the image to 500x500
        resized_image = cv2.resize(image, (500, 500))

        # write the image back to the file
        cv2.imwrite(full_path, resized_image)
