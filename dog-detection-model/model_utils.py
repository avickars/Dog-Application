from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import torch
from torchvision import transforms
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMAGE_SIZE = 448

def plot_tensor(image, box):
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Displaying the image 
    ax.imshow(image.permute(1, 2, 0))
    
    # Creating coordinates for the bounding box
    # CITATION: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
    # (XMin, YMin) * IMAGE_SIZE
    xy = box[[0,2]] * IMAGE_SIZE
    
    # (XMax - XMin) * IMAGE_SIZE
    width = (box[1] - box[0]) * IMAGE_SIZE
    # (YMax - YMin) * IMAGE_SIZE
    height = (box[3] - box[2]) * IMAGE_SIZE
    
    # Creating the bounding box
    rect = patches.Rectangle(xy=xy, 
                             width=width, 
                             height=height, 
                             linewidth=1, 
                             edgecolor='r', 
                             facecolor='none')
    # Adding the bounding box
    ax.add_patch(rect)
    
    # Displaying the image and bounding box
    plt.show()

imageTransforms = {
    'train': transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.4777, 0.4482, 0.3984], [0.2717, 0.2655, 0.2715])
    ]),
    'validation': transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.4777, 0.4482, 0.3984], [0.2717, 0.2655, 0.2715])
    ]),
    'test': transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.4777, 0.4482, 0.3984], [0.2717, 0.2655, 0.2715])
    ]),
}

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")




# class OpenImagesDataset(Dataset):
#     def __init__(self, rootDirectory, anchorBoxes, transform=None, dataType='train'):
#         # Root directory of the Open-Images Dataset
#         self.rootDirectory = rootDirectory
        
#         # Directory containing the images
#         self.imageDirectory = f"{self.rootDirectory}/{dataType}/data"
        
#         # The transformation of the images to apply
#         self.transform = transform
        
#         # The data set type (train/validation/test)
#         self.dataType = dataType
        
#         # Image labels (i.e. true bounding boxes)
#         self.labels = pd.read_csv(f"{rootDirectory}/{dataType}/labels/detections.csv", index_col=0)\
        
#         # List of imageIDs with no duplicates
#         self.imageList = self.labels['ImageID'].drop_duplicates()
        
#         # Pre-defined anchor box width/heights
#         with open(anchorBoxes, 'rb') as f:
#             self.anchorBoxes = np.load(f)
            
#     def __len__(self):
#         return len(self.imageList)
    
#     def __getitem__(self, index):
#         # Creating the path of the iamge
#         img_path = os.path.join(self.imageDirectory, f"{self.imageList.iloc[index]}.jpg")
        
#         # Reading in the image
#         image = Image.open(img_path)
        
#         # Transforming the image according to its datatype
#         image = imageTransforms[self.dataType](image)
        
        
        
        # return image, 1