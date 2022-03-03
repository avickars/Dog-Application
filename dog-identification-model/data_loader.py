from torch.utils.data import Dataset
import random
import os
import pandas as pd
from PIL import Image

class DogsDataSet(Dataset):
    def __init__(self, transform=None, dataType='train'):
        # Reading attributes
        self.dogList = pd.read_csv('attributes.csv')
        self.dogList = self.dogList[self.dogList['cleanImages'] >= 2]

        # Defining the image directory
        self.imageDirectory = 'dogs'

        # Reading in the boxes
        self.boxes = pd.read_csv('boxesDF.csv', index_col=0)

        # Transformations we are applying
        self.transform = transform

        # Data type we need ('train/validation/test')
        self.dataType = dataType

    def __len__(self):
        return len(self.dogList)

    def __getitem__(self, index):
        if self.dataType == 'train':
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

            if self.transform is not None:
                anchorImg = self.transform(anchorImg, anchorImgBox.values[0])
                positiveImg = self.transform(positiveImg, positiveImgBox.values[0])
                negativeImg = self.transform(negativeImg, negativeImgBox.values[0])

            return positiveImg, anchorImg, negativeImg
        else:
            # Creating the path of the target dog
            targetDogPath = self.dogList.iloc[index]['path']

            # Getting the number of available images of this dog
            numAvailableImages = self.dogList.iloc[index]['cleanImages']

            # Randomly decide if we want two images of the same dog or different dog
            isSame = random.sample(range(0, 2), 1)[0]

            # **************************** If we want 2 images of the same dog ****************************

            if isSame:
                # Randomly select 2 images from the available images
                targetImages = random.sample(range(0, numAvailableImages), 2)

                # Defining the path to the anchor image
                omg1Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[0]}.jpg")

                # Defining the path to the positive iamge
                omg2Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImages[1]}.jpg")

                # Reading in the anchor image
                img1 = Image.open(omg1Path).convert("RGB")

                # Getting the anchor img box coords
                img1Box = self.boxes[
                    (self.boxes['path'] == targetDogPath) &
                    (self.boxes['image'] == f"img_{targetImages[0]}.jpg")
                    ][['xmin', 'ymin', 'xmax', 'ymax']]

                # Reading in the anchor image
                img2 = Image.open(omg2Path).convert("RGB")

                # Getting the positive img box coords
                img2Box = self.boxes[
                    (self.boxes['path'] == targetDogPath) &
                    (self.boxes['image'] == f"img_{targetImages[1]}.jpg")
                    ][['xmin', 'ymin', 'xmax', 'ymax']]
            else:

                # Randomly select 2 images from the available images
                targetImage = random.sample(range(0, numAvailableImages), 1)[0]

                # Defining the path to the anchor image
                omg1Path = os.path.join(self.imageDirectory, f"{targetDogPath}/img_{targetImage}.jpg")

                # Reading in the anchor image
                img1 = Image.open(omg1Path).convert("RGB")

                # Getting the anchor img box coords
                img1Box = self.boxes[
                    (self.boxes['path'] == targetDogPath) &
                    (self.boxes['image'] == f"img_{targetImage}.jpg")
                    ][['xmin', 'ymin', 'xmax', 'ymax']]

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

            if self.transform is not None:
                img1 = self.transform(img1, img1Box.values[0])
                img2 = self.transform(img2, img2Box.values[0])

            return img1, img2



trainingData = DogsDataSet(dataType='test')
img1, img1Box = trainingData.__getitem__(1)