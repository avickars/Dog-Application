from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import torch
from torchvision import transforms
import os
from PIL import Image

IMAGE_SIZE = 448

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

class OpenImagesDataset(Dataset):
    def __init__(self, rootDirectory, anchorBoxes, transform=None, dataType='train'):
        # Root directory of the Open-Images Dataset
        self.rootDirectory = rootDirectory
        
        # Directory containing the images
        self.imageDirectory = f"{self.rootDirectory}/{dataType}/data"
        
        # The transformation of the images to apply
        self.transform = transform
        
        # The data set type (train/validation/test)
        self.dataType = dataType
        
        # Image labels (i.e. true bounding boxes)
        self.labels = pd.read_csv(f"{rootDirectory}/{dataType}/labels/detections.csv", index_col=0)\
        
        # List of imageIDs with no duplicates
        self.imageList = self.labels['ImageID'].drop_duplicates()
        
        # Pre-defined anchor box width/heights
        with open(anchorBoxes, 'rb') as f:
            self.anchorBoxes = np.load(f)
            
    def __len__(self):
        return len(self.imageList)
    
    def __getitem__(self, index):
        # Creating the path of the iamge
        img_path = os.path.join(self.imageDirectory, f"{self.imageList.iloc[index]}.jpg")
        
        # Reading in the image
        image = Image.open(img_path)
        
        # Transforming the image according to its datatype
        image = imageTransforms[self.dataType](image)
        
        
        
        return image, 1