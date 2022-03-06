import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_tensor(image, predictedBoxes=None, trueBoxes=None):
    """"Plots the decoded model output
    Args: 
        image (tensor): The image tensor
        predictedBoxes (tensor): Boxes predicted by the model ([[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]])
        trueBoxes (tensor): The true boxes ([[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]])
    Returns:
        Nothing
    """
    # Create figure and axes
    fig, ax = plt.subplots()
    
    # Displaying the image 
    ax.imshow(image.permute(1, 2, 0))

    if predictedBoxes is not None:
        # Creating coordinates for the bounding box
        # CITATION: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
        for box in predictedBoxes:

            xy = box[[0,1]]

            width = (box[2] - box[0])

            height = (box[3] - box[1])
            
            # Creating the bounding box
            rect = patches.Rectangle(xy=xy, 
                                    width=width, 
                                    height=height, 
                                    linewidth=1, 
                                    edgecolor='r', 
                                    facecolor='none')
            # Adding the bounding box
            ax.add_patch(rect)

    if trueBoxes is not None:
         # Creating coordinates for the bounding box
        # CITATION: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
        # (XMin, YMin) * IMAGE_SIZE
        for box in trueBoxes:
             # xy = box[[0,1]] * IMAGE_SIZE
        
            # width = (box[2] - box[0]) * IMAGE_SIZE

            # height = (box[3] - box[1]) * IMAGE_SIZE

            xy = box[[0,1]]

            width = (box[2] - box[0])

            height = (box[3] - box[1])
            
            
            # Creating the bounding box
            rect = patches.Rectangle(xy=xy, 
                                    width=width, 
                                    height=height, 
                                    linewidth=1, 
                                    edgecolor='g', 
                                    facecolor='none')
            # Adding the bounding box
            ax.add_patch(rect)
    
    # Displaying the image and bounding box
    plt.show()