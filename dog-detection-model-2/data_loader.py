from torch.utils.data import Dataset
import os
import pandas as pd
from PIL import Image
import torch
from model_transformations import normalize_box_coordinates

def collate_fn(batch):
    return tuple(zip(*batch))

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

        # Normalizing the box coordinates to [0,1]
        # Dropping everything we don't need
        # self.labels = normalize_box_coordinates(
        #     self.labels[['ImageID', 'XMin', 'XMax', 'YMin', 'YMax']], 
        #     self.labels['imageWidth'],
        #     self.labels['imageHeight'])
    
        # Becomes: [imageID...imageID]
        self.imageList = self.labels['ImageID'].drop_duplicates().reset_index(drop=True)
            
    def __len__(self):
        if self.dataType == 'train':
            return 1000
        else:
            return 100
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
        
        # Executing the transformations
        imageTensor, boxes = self.transform(image, boxes)
        
        # Turning the boxes into a tensor
        boxes = torch.from_numpy(boxes).to(torch.int64)
        
        # Extracting the number of dogs in the photo
        numDogs = boxes.shape[0]
        
        # Determining the area
        area = (boxes[:,2] - boxes[:,0])*(boxes[:,3] - boxes[:,1])
        
        # Determining the image ID by the index
        imageIDs = torch.tensor(index)
        
        classLabels = torch.ones((numDogs,), dtype=torch.int64)
        
        isCrowd = torch.zeros((numDogs,), dtype=torch.uint8)
        
        classLabels = torch.ones(boxes.shape[0], dtype=torch.int64)
        
        target = {}
        target['boxes'] = boxes
        target['labels'] = classLabels
        target['image_id'] = imageIDs
        target['area'] = area
        target['iscrowd'] = isCrowd
  
        return imageTensor, target