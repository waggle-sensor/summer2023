from torch import nn
import torch
class SRCNN(nn.Module):
    def __init__(self, channels):
        super(SRCNN, self).__init__()
        self.conv1 = nn.Conv2d(channels, out_channels=64, kernel_size=9, groups = 1, padding = (4,4))
        self.conv2 = nn.Conv2d(64, out_channels=32, kernel_size=1, groups= 1)
        self.conv3 = nn.Conv2d(32, out_channels=channels, kernel_size=5,groups=1, padding = (2,2))
        self.relu = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
       
        x = self.conv2(x)
      
        x = self.relu(x)
        x = self.conv3(x)
        return x
    
class PSNR(nn.Module):
    def __init__(self):
        super(PSNR,self).__init__()
        self.mse =  nn.MSELoss()
    def forward(self, img1, img2):
        mse = self.mse(img1,img2)
        max_pixel_value =255.0
        psnr = 20 * torch.log10(max_pixel_value / torch.sqrt(mse))
        return psnr
