from torchvision import transforms
from PIL import Image
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from params import IMAGE_SIZE

class Crop:
    def __call__(self, img, coords):
        """Crops the image according to its coords
        Args:
            img (pil): image to crop
            coords (list/tuple): [xmin, ymin, xmax,ymax]
        Returns:
            cropped img
        """
        return img.crop(coords), coords


class Transformations(object):
    """Execute the transformations and augmentations according to the datatype

    Args:
        imageSize (int): image size to resize images to
        dataType (1 of train/validation/test): defines which transformations to apply
        probs: (list of floats btw 0 and 1): defines probabilities for each transformation
        
    Return:
        image and coords
    """
    def __init__(self, dataType='train', probs={'RandomHorizontalFlip':0.5,'RandomVerticalFlip':0.5}):

        # Defining the resize transformation
        # self.resize = Resize(IMAGE_SIZE)
        
        # Defining the random horizontal flip
        self.randomHorizontalFlip = RandomHorizontalFlip(probs['RandomHorizontalFlip'])

        # Defining the random horizontal flip
        self.randomVerticalFlip = RandomVerticalFlip(probs['RandomVerticalFlip'])

        # Defining tensor transformation
        self.toTensor = ToTensor()

        self.crop = Crop()

        self.resize = Resize(imageSize=IMAGE_SIZE)
        
        # Defining them in list according to data type
        self.transormations = {
            'train': [
                self.crop,
                # self.randomHorizontalFlip,
                # self.randomVerticalFlip,
                self.resize,
                self.toTensor
                ],
            'validation': [
                self.crop,
                self.resize,
                self.toTensor
                ],
            'test': [
                self.crop,
                self.resize,
                self.toTensor
                ]
            }
                
        
        # Recording the datatype
        self.dataType = dataType
        
    def __call__(self, image, coords):
        # Executing the transormations according to the data type
        for transformation in self.transormations[self.dataType]:
            image, coords = transformation(image, coords)
        return image


class ToTensor():
    """ Turns the PIL Image into a tensor
    Args:
        image (PIL): the image to change
        coords (np.array): array of box coord just passing through
   
    """
    def __init__(self):
        self.tensor = transforms.ToTensor()
    def __call__(self, image, coords):
        return self.tensor(image), coords

class RandomHorizontalFlip(object):
    """Randomly horizontally flips the Image with the probability *p*
    
    Parameters
    ----------
    p: float
        The probability with which the image is flipped
        
    image: PIL
            The image to flip
    
    coords: ndarray
            The coords of the bound box (xmin, xmax, ymin, ymax)
        
        
    Returns
    -------
    
    image: PIL
        Flipped image 
    
    coords: numpy.ndarray
        Tranformed bounding box co-ordinates of the format `n x 4` where n is 
        number of bounding boxes and 4 represents `x1,y1,x2,y2` of the box
        
    """
    
    def __init__(self, p=0.5):
        assert isinstance(p, float)
        assert (p <= 1) & (p >= 0)
        self.p = p
        
    def __call__(self, image, coords):
        if np.random.choice([0,1], p=[1-self.p,self.p]):
            
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        return image, coords

    
class RandomVerticalFlip(object):
    """Randomly vertically flips the Image with the probability *p*

    Parameters
    ----------
    p: float
        The probability with which the image is flipped

    image: PIL
            The image to flip

    coords: ndarray
            The coords of the bound box (xmin, xmax, ymin, ymax)


    Returns
    -------

    image: PIL
        Flipped image 

    coords: numpy.ndarray
        Tranformed bounding box co-ordinates of the format `n x 4` where n is 
        number of bounding boxes and 4 represents `x1,y1,x2,y2` of the box

    """

    def __init__(self, p=0.5):
        assert isinstance(p, float)
        assert (p <= 1) & (p >= 0)
        self.p = p

    def __call__(self, image, coords):
        if np.random.choice([0,1], p=[1-self.p,self.p]):
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        return image, coords


class Resize(object):
    # CITATION: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html#transforms
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self, imageSize):
        assert isinstance(imageSize, int)
        self.imageSize = imageSize
        self.transform = transforms.Resize((self.imageSize, self.imageSize))
    
        
    def __call__(self, image, coords):        
        image = self.transform(image)
        return image, coords     