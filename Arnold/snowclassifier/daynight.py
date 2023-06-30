import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt
values = []
for root, dirs, files in os.walk(".\images\W014"):
    for file in files:
        path = os.path.join(root, file)
        
        image = cv.imread(path)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY )
        
        values.append(np.average(image))
        if np.average(image) <90 and np.average(image) > 70:
            cv.imwrite('image.jpeg', cv.imread(path))
        
print('plotting')
counts, bins, patches = plt.hist(values)
for count, patch in zip(counts, patches):
    plt.annotate(str(int(count)), xy=(patch.get_x() + patch.get_width() / 2, patch.get_height()),
                 xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
plt.title('Brightness')

# Display the chart
plt.show()
    