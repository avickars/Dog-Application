from torch.utils.data import Dataset
import torch
import pandas as pd
from model_transformations import normalize_box_coordinates
from PIL import Image
import os
import numpy as np
from iou_yolo import iou_yolo

class OpenImagesDataset(Dataset):
    def __init__(self, rootDirectory, anchorBoxes, transform=None, dataType='train', gridSize=3, imageSize=448):
        # Root directory of the Open-Images Dataset
        self.rootDirectory = rootDirectory
        
        # Defining the gridSize*gridSize applied to every image
        self.gridSize = gridSize
        
        # Directory containing the images
        self.imageDirectory = f"{self.rootDirectory}/{dataType}/data"
        
        # The data set type (train/validation/test)
        self.dataType = dataType
        
        # The transformation of the images to apply
        self.transform = transform(imageSize=imageSize, dataType=self.dataType)
        
        # Image labels (i.e. true bounding boxes)
        self.labels = pd.read_csv(f"{rootDirectory}/{dataType}/labels/detections.csv", index_col=0)
        
        # Normalizing the box coordinates to [0,1]
        # Dropping everything we don't need
        self.labels = normalize_box_coordinates(
            self.labels[['ImageID', 'XMin', 'XMax', 'YMin', 'YMax']], 
            self.labels['imageWidth'],
            self.labels['imageHeight'])
        
        # List of imageIDs with no duplicates
        # Becomes: [imageID...imageID]
        self.imageList = self.labels['ImageID'].drop_duplicates().reset_index(drop=True)
        
        # Pre-defined anchor box width/heights
        # [(Width, Heights)...(Width, Heights)]
        with open(anchorBoxes, 'rb') as f:
            self.anchorBoxes = np.load(f)
            
        self.numAnchorBoxes = self.anchorBoxes.shape[0]
            
    def __len__(self):
        return len(self.imageList)
    
    def __getitem__(self, index):
        # Creating the path of the iamge
        img_path = os.path.join(self.imageDirectory, f"{self.imageList[index]}.jpg")
        
        # Reading in the image
        image = Image.open(img_path)
        
        # Extracting the boxes in this image
        # Dropping ImageID
        boxes = self.labels[
            self.labels['ImageID'] == self.imageList[index]
        ].drop('ImageID',axis=1).values
        
        input, boxes = self.transform(image, boxes)
        
        label = self.__create_label(boxes)

        return input, label
    
        
    def __create_label(self, boxes):
        """Creates the Y values of the model
        
        Args: boxes(np.array): [[xmin, xmax, ymin, ymax]...[xmin, xmax, ymin, ymax]]
        
        Return:
            
        """
        # Initializing a tensor to hold the y values
        y = torch.zeros((self.gridSize, self.gridSize, self.numAnchorBoxes*5))
        
        # Executing this outside the for loop for extra speed
        # Computing the width/height of all boxes
        # (xmax - xmin)
        objectsWidth = boxes[:,1] - boxes[:,0]
        # (ymax - ymin)
        objectsHeight = boxes[:,3] - boxes[:,2]
        
        # Computing the center coords of the boxes
        # (width/2)+xmin
        xObjectsCenter = objectsWidth/2 + boxes[:,0]
        # (width/2)+ymax
        yObjectsCenter = objectsHeight/2 + boxes[:,2]
                
        # Iterating through each box in the image (there may be multiple)
        # NOTE: in the freek case where the center of two objects are in the same grid cell and have the 
        # same best anchor box, we take the second automatically as the values of the first will
        # be overwritten by the second
        for i in range(0, boxes.shape[0]):
            # Selecting the box (and its width/height and center location) to work with 
            objectWidth = objectsWidth[i]
            objectHeight = objectsHeight[i]
            xObjectCenter = xObjectsCenter[i]
            yObjectCenter = yObjectsCenter[i]

            print('XCenter:',xObjectCenter)
            print('YCenter:',yObjectCenter)
            
            # Computing the IOUs for all anchor boxes
            ious = iou_yolo([objectWidth, objectHeight], self.anchorBoxes)
            
            # Computing the best anchor box (highest IOU with the object)
            bestAnchorBox = np.argmax(ious)

            # Computing the best IOU that corresponds with the bestAnchorBox
            bestAnchorBoxIOU = np.max(ious)

            # Getting the best anchor box width/height    
            bestAnchorBoxWidth = self.anchorBoxes[bestAnchorBox,0]
            bestAnchorBoxHeight = self.anchorBoxes[bestAnchorBox,1]

            # Computing the width/height of object relative to the best anchor box
            relativeWidth = objectWidth / bestAnchorBoxWidth
            relativeHeight = objectHeight / bestAnchorBoxHeight
                        
            # Computing the grid cell each box falls into 
            gridCellRow = (yObjectCenter * self.gridSize).astype(int)
            gridCellCol = (xObjectCenter * self.gridSize).astype(int)
            
            # Computing the location of the center point relative to the grid cell
            xGridCell = xObjectCenter * self.gridSize - gridCellCol
            yGridCell = yObjectCenter * self.gridSize - gridCellRow
            
            # Assigning object to its grid cell / Best Anchor Box
            y[ 
                gridCellRow, 
                gridCellCol,
                bestAnchorBox*5:bestAnchorBox*5+5
            ] = torch.tensor([1, yGridCell, xGridCell, relativeWidth, relativeHeight])
        return y