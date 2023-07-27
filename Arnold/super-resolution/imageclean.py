import os

print(os.getcwd())
for root, dirs, files in os.walk('.\DIV2K\DIV2K_valid_LR_bicubic_X2'):
    for file in files:
        print(file)
        path = os.path.join(root, file)
        os.rename(path, os.path.join(root, f'{file[1:4]}.png'))