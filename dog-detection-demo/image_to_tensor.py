from PIL import Image
from torchvision import transforms

def to_tensor(images):
    """
    Scales image pixels to [0,1] and converts to tensor

    Args:
        images (list): list of image paths

    Return:
        transformedImages (list): list of images in tensor form

    """

    # Defining empty list to hold loaded images
    loadedImages = []
    
    # Loading the images
    for image in images:
        loadedImages.append(Image.open(image).convert("RGB"))
    
    # Defining the transform to tensor (converts to tensor and scale pixels to [0,1])
    toTensor = transforms.ToTensor()
    
    # Defining empty list to hold transformed images
    transformedImages = []
    for image in loadedImages:
        transformedImages.append(toTensor(image))

    return transformedImages