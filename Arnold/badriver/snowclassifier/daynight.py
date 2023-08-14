import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt
values = []
for root, dirs, files in os.walk(".\snowclassifier\images\snowmodelimages"):
    for file in files:
        path = os.path.join(root, file)
        image = cv.imread(path)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY )
        
        values.append(np.average(image))
        if('nosnow' in path):
            if np.average(image) > 50:
                cv.imwrite(f".\snowclassifier\images/time/nosnow/day/{file}", cv.imread(path))
            else:
                cv.imwrite(f".\snowclassifier\images/time/nosnow/night/{file}", cv.imread(path))
        else:
            if np.average(image) > 50:
                cv.imwrite(f".\snowclassifier\images/time/snow/day/{file}", cv.imread(path))
            else:
                cv.imwrite(f".\snowclassifier\images/time/snow/night/{file}", cv.imread(path))
print('plotting')
counts, bins, patches = plt.hist(values)
for count, patch in zip(counts, patches):
    plt.annotate(str(int(count)), xy=(patch.get_x() + patch.get_width() / 2, patch.get_height()),
                 xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
plt.title('Brightness')

# Display the chart
plt.show()
    