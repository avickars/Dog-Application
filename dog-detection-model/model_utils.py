import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from params import IMAGE_SIZE


def plot_image(image, boxes):
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Displaying the image 
    ax.imshow(image)
    
    # Creating coordinates for the bounding box
    # CITATION: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
    # (XMin, YMin) * IMAGE_SIZE
    for box in boxes:
        xy = box[[0,2]] * IMAGE_SIZE
        
        # (XMax - XMin) * IMAGE_SIZE
        width = (box[1] - box[0]) * IMAGE_SIZE
        # (YMax - YMin) * IMAGE_SIZE
        height = (box[3] - box[2]) * IMAGE_SIZE
        
        # Creating the bounding box
        rect = patches.Rectangle(xy=xy, 
                                width=width, 
                                height=height, 
                                linewidth=1, 
                                edgecolor='r', 
                                facecolor='none')
        # Adding the bounding box
        ax.add_patch(rect)
    
    # Displaying the image and bounding box
    plt.show()

def plot_tensor(image, boxes):
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Displaying the image 
    ax.imshow(image.permute(1, 2, 0))
    
    # Creating coordinates for the bounding box
    # CITATION: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
    # (XMin, YMin) * IMAGE_SIZE
    for box in boxes:
        xy = box[[0,2]] * IMAGE_SIZE
        
        # (XMax - XMin) * IMAGE_SIZE
        width = (box[1] - box[0]) * IMAGE_SIZE
        # (YMax - YMin) * IMAGE_SIZE
        height = (box[3] - box[2]) * IMAGE_SIZE
        
        # Creating the bounding box
        rect = patches.Rectangle(xy=xy, 
                                width=width, 
                                height=height, 
                                linewidth=1, 
                                edgecolor='r', 
                                facecolor='none')
        # Adding the bounding box
        ax.add_patch(rect)
    
    # Displaying the image and bounding box
    plt.show()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")