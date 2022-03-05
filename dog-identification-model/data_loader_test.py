from torch.utils.data import Dataset
import random
import os
import pandas as pd
from PIL import Image
from data_transformations import Transformations

class DogsDataSet_Test(Dataset):
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

        # Randomly select 2 images from the available images
        targetImages = random.sample(range(0, numAvailableImagesTarget), 2)

        # Defining the path to the anchor image
        omg1Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[0]}.jpg")

        # Reading in the anchor image
        img1 = Image.open(omg1Path).convert("RGB")

        # Getting the anchor img box coords
        img1Box = self.boxes[
            (self.boxes['path'] == targetDogPath) &
            (self.boxes['image'] == f"img_{targetImages[0]}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]

        # **************************** If we want 2 images of the same dog ****************************

        if isSame:
            # Defining the path to the positive iamge
            omg2Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[1]}.jpg")

            # Reading in the anchor image
            img2 = Image.open(omg2Path).convert("RGB")

            # Getting the positive img box coords
            img2Box = self.boxes[
                (self.boxes['path'] == targetDogPath) &
                (self.boxes['image'] == f"img_{targetImages[1]}.jpg")
                ][['xmin', 'ymin', 'xmax', 'ymax']]

            # Defining label (i.e. they are the same)
            label = 0
        else:
            # Choosing the dog to use as the different dog
            # Making sure we are not using the same dog as above
            while True:
                img2Index = random.sample(range(0, self.__len__()), 1)[0]
                if img2Index != index:
                    break

            # Creating the path of the target dog
            omg2Path = self.dogList.iloc[img2Index]['path']

            # Getting the number of available images of this dog
            numAvailableImages = self.dogList.iloc[img2Index]['cleanImages']

            # Randomly select 1 images from the available images
            img2Image = random.sample(range(0, numAvailableImages), 1)[0]

            # Defining the path to the anchor image
            ogm2PathFull = os.path.join(self.imageDirectory, f"{omg2Path}/img_{img2Image}.jpg")

            # Reading in the anchor image
            img2 = Image.open(ogm2PathFull).convert("RGB")

            # Getting the negative img box coords
            img2Box = self.boxes[
                (self.boxes['path'] == omg2Path) &
                (self.boxes['image'] == f"img_{img2Image}.jpg")
                ][['xmin', 'ymin', 'xmax', 'ymax']]

            label = 1

        img1 = self.transform(img1, img1Box.values[0])
        img2 = self.transform(img2, img2Box.values[0])

        return img1, img2, label

