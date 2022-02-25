import numpy as np
from iou import IOU
import torch

class NonMaxSurpression(object):
    # CITATION: https://www.youtube.com/watch?v=YDkjWEN8jNA&list=PLhhyoLH6Ijfw0TpCTVTNk42NN08H6UvNq&index=3&t=117s
    """Executes non max surpression on the model output
    __init__:
        Args: 
            probThreshold (float): threshold used to determine if box even contains an object
            iousThreshold (float): theshold used to determine if boxes are the same object
    __call__:
        Args:
            target(tensor/array): Model output of form (batchSize, gridSize, gridSize, 5*NumAnchorBoxes)
        Return:
            boxes (list): List of boxes to output for each batch.  Has same form as reshaped target
    """
    def __init__(self, probThreshold=0.6, iouThreshold=0.5):
        self.probThreshold = probThreshold
        self.iouThreshold = iouThreshold

    def __call__(self, target):
        """
        Reshaping target array to this list structure:
            batch
                - box1
                - box2
                ...
            batch
                - box1
                - box2
                ...        
        """
        target = target.reshape((target.shape[0], -1, 5)).tolist()
        
        boxesAllBatches = []
        
        # Iterating through each batch
        for batch in target:
            batchBoxes = []
            
            # Extracting the boxes that meet the initial probability of object threshold
            boxes = [box for box in batch if box[0] > self.probThreshold]

            # Sorting the boxes in descending order with respect to theprobability of object
            boxes = sorted(boxes, key=lambda x: x[0], reverse=True)

            # While there are still boxes to check
            while boxes:                
                # Popping off the best box
                chosenBox = np.array(boxes.pop(0))

                # Appending to the list of boxes
                batchBoxes.append(torch.tensor(chosenBox))

                # Testing if there are any more boxes to consider
                if len(boxes) > 0:
                    # Computing the IOU between this box and all others
                    ious = IOU(chosenBox, np.array(boxes))
                    
                    # Checking if the boxes are under the IOU threshold
                    meetsIOUThreshold = (ious < self.iouThreshold).nonzero()[0]
                    
                    # If under the threshold, we keep them otherwise we discard the,
                    boxes = [boxes[i] for i in meetsIOUThreshold]
                
            # Appending the list of boxes for this batch
            boxesAllBatches.append(batchBoxes)
        return boxesAllBatches