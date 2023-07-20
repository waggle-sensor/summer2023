from  sage_data_client import query
import os
from torchvision import transforms, models, datasets
import torch
transformation = transforms.Compose([transforms.Resize((224,224)),
                                     transforms.ToTensor()
                                    ])
dataset = datasets.ImageFolder("images\W083", transformation)
print(dataset.imgs[0][0][23:42][0][0][23:42])
image_loader = torch.utils.data.DataLoader(dataset, batch_size = 1)
data =query(
    start= "2023-02-01T01:00:00Z",
  end= "2023-06-10T01:00:00Z",
  filter = {
    "name" : "upload",
        "vsn": "W083",
        "plugin" : "registry.sagecontinuum.org/theone/imagesampler:0.3.0",
	"task" : "imagesampler-bottom"
    })
print(data['value'])
data['image'] = ''
data['snow'] = ''
print(data)
for i, (img, l) in enumerate(image_loader):
    if l ==2:
        break
    else:
        name = dataset.imgs[i][0][23:42]
        row = data['value'].str.contains(name)
        
        row_index = data[row].index[0]
        print(row_index)
      
        data.loc[row_index, 'image'] = img.numpy()
        

