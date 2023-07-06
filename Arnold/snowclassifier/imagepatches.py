import cv2 as cv
import os
import numpy
global snow
snow = -1
def mouse_click(event, x, y, 
                flags, param):
    global snow  
   #no snow
    if event == cv.EVENT_LBUTTONDOWN:
        snow = 0
    #can't tell
    if event == cv.EVENT_MBUTTONDOWN:
        snow = 2
    #s                                  now
    if event == cv.EVENT_RBUTTONDOWN:
        snow = 1
    
        
    
no_snow = True        
for root, dirs, files in os.walk("C:/Users/alxto/Desktop/SAGE/summer2023/Arnold/snowclassifier/images/snowmodelimages/nosnow"):
    for num,file in enumerate(files):
        
        print(f'File {num}/{len(files)}')
        
        path = os.path.join(root, file)
        
        image = cv.imread(path)
      
        height, width = image.shape[:2]
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
            if(no_snow):
                cv.imwrite(f'./snowclassifier/images/patches/nosnow/{file}-{j+1}.jpeg', part)
                continue
                 
            cv.imshow(f"{file} {j+1}", part)
            cv.setMouseCallback(f"{file} {j+1}", mouse_click)
            cv.waitKey(0)
            cv.destroyAllWindows()
           
            if snow == 0:
                cv.imwrite(f'./snowclassifier/images/patches/nosnow/{file}-{j+1}.jpeg', part)
            
            if snow == 1:
                cv.imwrite(f'./snowclassifier/images/patches/snow/{file}-{j+1}.jpeg', part)
            if snow == 2:
                cv.imwrite(f'./snowclassifier/images/patches/unclear/{file}-{j+1}.jpeg',part)
            
            







# Wait for key press and close the windows

