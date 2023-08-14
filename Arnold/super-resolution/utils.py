import torch
from torchvision import transforms
from math import log10,sqrt
import numpy as np
def random_crop_image_pair(high_res_tensor, low_res_tensor, crop_size, scale_factor):
    transform = transforms.RandomCrop(crop_size)
    
    # Convert tensors to PIL images
    high_res_image = transforms.ToPILImage()(high_res_tensor)
    low_res_image = transforms.ToPILImage()(low_res_tensor)

    # Generate random crop coordinates once
    i, j, h, w = transform.get_params(high_res_image, output_size=(crop_size, crop_size))

    # Apply the same random crop to both images
    high_res_cropped = transforms.functional.crop(high_res_image, i, j, h, w)
    low_res_cropped = transforms.functional.crop(low_res_image, i//scale_factor, j//scale_factor, h//scale_factor, w//scale_factor)

    # Convert back to tensors
    high_res_cropped = transforms.ToTensor()(high_res_cropped)
    low_res_cropped = transforms.ToTensor()(low_res_cropped)

    return low_res_cropped, high_res_cropped

def PSNR_func(img1, img2):
    mse = np.mean(((img1 - img2) **2))
    if(mse ==0):
        return 100
    
   
    psnr = 20 * log10(255.0 / sqrt(mse))
    return psnr