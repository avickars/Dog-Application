from PIL import Image
from torchvision import transforms
import torch

IMAGE_SIZE = 448

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

    def __call__(self, image):
        image = self.transform(image)
        return image


class Crop:
    def __call__(self, img, coords):
        """Crops the image according to its coords
        Args:
            img (pil): image to crop
            coords (list/tuple): [xmin, ymin, xmax,ymax] - output of dog-detection model
        Returns:
            cropped img
        """
        return img.crop(coords)


def load_and_transform(imageLinks, coordinates):
    """
    Scales image pixels to [0,1] and converts to tensor

    Args:
        images (list): list of image paths
        coordinates (list): [[xmin, ymin, xmax,ymax],...,[xmin, ymin, xmax,ymax]]

    Return:
        transformedImages (list): list of images in tensor form

    """

    # Defining empty list to hold loaded images
    loadedImages = []

    # Defining image resize
    resize = Resize(imageSize=IMAGE_SIZE)

    # Defining image crop
    crop = Crop()

    # Loading the images
    for i in range(0, len(imageLinks)):
        # Loading the images
        loadedImage = Image.open(imageLinks[i]).convert("RGB")

        # Cropping the images by the coordinates
        croppedImage = crop(loadedImage, coordinates[i])

        # Resizing the images
        loadedImages.append(resize(croppedImage))

    # Defining the transform to tensor (converts to tensor and scale pixels to [0,1])
    toTensor = transforms.ToTensor()

    # Defining empty list to hold transformed images
    transformedImages = []
    for image in loadedImages:
        transformedImages.append(toTensor(image))

    return torch.stack(transformedImages)