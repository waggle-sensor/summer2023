import os 
from core import *
from matplotlib.pyplot import imread, imsave
from torchvision import transforms
from PIL import Image
import random
print(os.getcwd())

for root, dirs, files in os.walk("./signs/trainHR"):
    for file in files:
        image = Image.open(os.path.join(root, file))
        image = transforms.ToTensor()(image)
        image = imresize(image, 0.5)
        image = transforms.ToPILImage()(image)
        image.save(f"./signs/trainLR/{file}")

# for root, dirs, files in os.walk("./signs/trainHR"):
#     for i, file in enumerate(files):
#         print(i)
#         os.rename(os.path.join(root, file), os.path.join(root, f"{i}.png"))
#         # os.rename( f"./signs/trainLR/{file}0", f"./signs/trainLR/{i}.png")