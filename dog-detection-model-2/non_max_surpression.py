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
            target(list):
            [dict:{
                    - boxes: [[xmin, ymin, xmax, ymax]...[xmin, ymin, xmax, ymax]]
                    - labels: [1,...1]
                    - scores: [s1, s2,...sN]
                
                }...]
        Return:
            the updated target list
    """
    def __init__(self, probThreshold=0.6, iouThreshold=0.5):
        self.probThreshold = probThreshold
        self.iouThreshold = iouThreshold

    def __call__(self, targets):
        for i in range(0,len(targets)):
            # Subsetting to the bound boxes
            bBoxes = targets[i]['boxes'].tolist()
            
            # Subsetting to the box scores
            probObject = targets[i]['scores'].tolist()
            
            # Merging the lists element wise
            bBoxAndProb = [[probObject[i]] + bBoxes[i] for i in range(0,len(bBoxes))]
        
            # Extracting the boxes that meet the initial probability of object threshold
            bBoxAndProb = [box for box in bBoxAndProb if box[0] > self.probThreshold]

            # Sorting the boxes in descending order with respect to theprobability of object
            bBoxAndProb = sorted(bBoxAndProb, key=lambda x: x[0], reverse=True)
            
            chosenBoxes = []
            
            # While there are still boxes to check
            while bBoxAndProb:                
                # Popping off the best box
                chosenBox = torch.tensor(bBoxAndProb.pop(0))

                # Appending to the list of boxes
                chosenBoxes.append((chosenBox))

                # Testing if there are any more boxes to consider
                if len(bBoxAndProb) > 0:
                    # Computing the IOU between this box and all others
                    ious = IOU(chosenBox, torch.tensor(bBoxAndProb))
                    
                    # Checking if the boxes are under the IOU threshold
                    meetsIOUThreshold = (ious < self.iouThreshold).nonzero()[0]
                    
                    # If under the threshold, we keep them otherwise we discard them,
                    bBoxAndProb = [bBoxAndProb[i] for i in meetsIOUThreshold]                  
            
 
            
            targets[i]['boxes'] = torch.stack([chosenBox[1:] for chosenBox in chosenBoxes])
            targets[i]['labels'] = torch.tensor([1 for chosenBox in chosenBoxes])
            targets[i]['scores'] = torch.tensor([chosenBox[0].item() for chosenBox in chosenBoxes])
            

        return targets
    