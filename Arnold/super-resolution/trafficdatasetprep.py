import os 
from core import *
from matplotlib.pyplot import imread, imsave
from torchvision.io import read_image, write_jpeg
print(os.getcwd())
for root, dirs, files in os.walk('./traffic/validLR'):
    for i, file in enumerate(files):
        path = os.path.join(root, file)
        value = int(file[:-4])
        print(value)
        if(value > 2195):
            os.remove(path)
        