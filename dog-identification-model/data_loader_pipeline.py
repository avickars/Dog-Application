import torch
from torch.utils.data import Dataset
import random
import os
import pandas as pd
from PIL import Image
from data_transformations import Transformations

class DogsDataSet_Test_Pipeline(Dataset):
    def __init__(self, dataType='train'):
        # Reading attributes
        self.dogList = pd.read_csv('attributes.csv')
        self.dogList = self.dogList[self.dogList['type'] == dataType]
        self.dogList = self.dogList.reset_index(drop=True)

        # Defining the image directory
        self.imageDirectory = 'dogs'

        # Reading in the boxes
        self.boxes = pd.read_csv('boxesDF.csv', index_col=0)

        # Transformations we are applying
        self.transform = Transformations(dataType)

        # Data type we need ('train/validation/test')
        self.dataType = dataType

    def __len__(self):
        return len(self.dogList)



    def __getitem__(self, index):
        # Creating the path of the target dog
        targetDogPath = self.dogList.iloc[index]['path']

        # Getting the number of available images of this dog
        numAvailableImagesTarget = self.dogList.iloc[index]['cleanImages']

        # Randomly decide if we want two images of the same dog or different dog
        isSame = random.sample(range(0, 2), 1)[0]

        # Setting random seed
        random.seed(1)

        # Randomly select 2 images from the available images
        targetImages = random.sample(range(0, numAvailableImagesTarget), 2)

        # GETTING 1st IMAGE

        # Defining the path to the anchor image
        omg1Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[0]}.jpg")

        # Reading in the anchor image
        img1 = Image.open(omg1Path).convert("RGB")

        # Getting the anchor img box coords
        img1Box = self.boxes[
            (self.boxes['path'] == targetDogPath) &
            (self.boxes['image'] == f"img_{targetImages[0]}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]

        # GETTING 2nd IMAGE

        # Defining the path to the positive iamge
        omg2Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[1]}.jpg")

        # Reading in the anchor image
        img2 = Image.open(omg2Path).convert("RGB")

        # Getting the positive img box coords
        img2Box = self.boxes[
            (self.boxes['path'] == targetDogPath) &
            (self.boxes['image'] == f"img_{targetImages[1]}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]

        img1_transformed = self.transform(img1, img1Box.values[0])
        img2_transformed = self.transform(img2, img2Box.values[0])

        return img1_transformed, img2_transformed, img1, img2, targetDogPath

