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
    
        
    
        
for root, dirs, files in os.walk(".\images\W014\snowW014"):
    for file in files:
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
        for i, part in enumerate(parts):
            if(i < 4):
                cv.imwrite(f'./images/patches/nosnow/{file}-{i+1}.jpeg', part)
                continue
            cv.imshow(f"Part {i+1}", part)
            cv.setMouseCallback(f"Part {i+1}", mouse_click)
            cv.waitKey(0)
            cv.destroyAllWindows()
           
            if snow == 0:
                cv.imwrite(f'./images/patches/nosnow/{file}-{i+1}.jpeg', part)
            
            if snow == 1:
                cv.imwrite(f'./images/patches/snow/{file}-{i+1}', part)
            if snow == 2:
                cv.imwrite(f'./images/patches/unclear/{file}-{i+1}',part)
            
            







# Wait for key press and close the windows

