from torch.utils.data import Dataset
import os
import pandas as pd
from PIL import Image

class OpenImagesDataset(Dataset):
    def __init__(self, rootDirectory, transform=None, dataType='train'):
        # Root directory of the Open-Images Dataset
        self.rootDirectory = rootDirectory
        
        # Directory containing the images
        self.imageDirectory = f"{self.rootDirectory}/{dataType}/data"
        
        # The data set type (train/validation/test)
        self.dataType = dataType
        
        # The transformation of the images to apply
        self.transform = transform(dataType=self.dataType)
        
        # Image labels (i.e. true bounding boxes)
        self.labels = pd.read_csv(f"{rootDirectory}/{dataType}/labels/detections.csv", index_col=0)
    
        # Becomes: [imageID...imageID]
        self.imageList = self.labels['ImageID'].drop_duplicates().reset_index(drop=True)
            
    def __len__(self):
        return len(self.imageList)
    
    def __getitem__(self, index):
        # Creating the path of the iamge
        img_path = os.path.join(self.imageDirectory, f"{self.imageList[index]}.jpg")
        
        # Reading in the image
        # They should already be all RGB, but just in case
        image = Image.open(img_path).convert("RGB")
        
        # Extracting the boxes for this image
        boxes = self.labels[self.labels['ImageID'] == self.imageList[index]]
        
        # Defining it just as an array
        boxes = boxes[['XMin','YMin', 'XMax','YMax']].values
        
        imageTensor, boxes = self.transform(image, boxes)
  
        return imageTensor, boxes