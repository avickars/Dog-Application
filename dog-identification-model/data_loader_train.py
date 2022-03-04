from torch.utils.data import Dataset
import random
import os
import pandas as pd
from PIL import Image
from data_transformations import Transformations

class DogsDataSet_Train(Dataset):
    def __init__(self, dataType='train'):
        # Reading attributes
        self.dogList = pd.read_csv('attributes.csv')
        self.dogList = self.dogList[self.dogList['cleanImages'] >= 2]
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
        # **************************** Extracting Target Images ****************************

        # Creating the path of the target dog
        targetDogPath = self.dogList.iloc[index]['path']

        # Getting the number of available images of this dog
        numAvailableImages = self.dogList.iloc[index]['cleanImages']

        # Randomly select 2 images from the available images
        targetImages = random.sample(range(0, numAvailableImages), 2)

        # Defining the path to the anchor image
        anchorImgPath = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[0]}.jpg")

        # Defining the path to the positive iamge
        positiveImgPath = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[1]}.jpg")

        # Reading in the anchor image
        anchorImg = Image.open(anchorImgPath).convert("RGB")

        # Getting the anchor img box coords
        anchorImgBox = self.boxes[
            (self.boxes['path'] == targetDogPath) &
            (self.boxes['image'] == f"img_{targetImages[0]}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]

        # Reading in the anchor image
        positiveImg = Image.open(positiveImgPath).convert("RGB")

        # Getting the positive img box coords
        positiveImgBox = self.boxes[
            (self.boxes['path'] == targetDogPath) &
            (self.boxes['image'] == f"img_{targetImages[1]}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]

        # **************************** Extracting Negative Image ****************************

        # Choosing the dog to use as the negative
        # Making sure we are not using the same dog as above
        while True:
            negativeImgIndex = random.sample(range(0, self.__len__()), 1)[0]
            if negativeImgIndex != index:
                break

        # Creating the path of the target dog
        negativeDogPath = self.dogList.iloc[negativeImgIndex]['path']

        # Getting the number of available images of this dog
        numAvailableImages = self.dogList.iloc[negativeImgIndex]['cleanImages']

        # Randomly select 1 images from the available images
        negativeImage = random.sample(range(0, numAvailableImages), 1)[0]

        # Defining the path to the anchor image
        negativeImgPath = os.path.join(self.imageDirectory, f"{negativeDogPath}/img_{negativeImage}.jpg")

        # Reading in the anchor image
        negativeImg = Image.open(negativeImgPath).convert("RGB")

        # Getting the negative img box coords
        negativeImgBox = self.boxes[
            (self.boxes['path'] == negativeDogPath) &
            (self.boxes['image'] == f"img_{negativeImage}.jpg")
            ][['xmin', 'ymin', 'xmax', 'ymax']]


        anchorImg = self.transform(anchorImg, anchorImgBox.values[0])
        positiveImg = self.transform(positiveImg, positiveImgBox.values[0])
        negativeImg = self.transform(negativeImg, negativeImgBox.values[0])

        return positiveImg, anchorImg, negativeImg
