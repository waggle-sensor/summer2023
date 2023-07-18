import cv2 
import os
import numpy as np
import pandas as pd
no_snow = True        
metadata = pd.read_csv('./metadata.csv')
for index, file in metadata.iterrows():
    if file['node'] != 'W083':
        continue
    path = file['path'] 
    
    image = cv2.imread(path)
    height, width = image.shape[:2]
    image = image[200:,:]
    
    # Calculate the width and height of each part
    part_width = width // 4
    part_height = height // 4

    # Split the image into 16 parts
    parts = []
    for i in range(4):
        for j in range(4):
            x = j * part_width
            y = i * part_height
            part = image[y:y + part_height, x:x + part_width]
            parts.append(part)
    for j, part in enumerate(parts):
        if file['node'] == 'W014':
            cv2.imwrite(f'./images/patches/W014/{j}/{file["name"][:-4]}-{j}.jpg',part)
        else:
            cv2.imwrite(f'./images/patches/W083/{j}/{file["name"][:-4]}-{j}.jpg',part)
    
            
            







# Wait for key press and close the windows

