from collections import Counter
import torch
from iou import IOU

def MAP(predBoxes, trueBoxes, iouThreshold=0.5):
    # CITATION: https://www.youtube.com/watch?v=FppOzcDvaDI&t=1193s
    # Flattening the predicted boxes
    predBoxFlatten = []
    for index, boxes in enumerate(predBoxes):
        for box in boxes:
            predBoxFlatten.append([index, box])
            
    # Flattening the true boxes
    trueBoxesFlatten = []
    for index, boxes in enumerate(trueBoxes):
        for box in boxes:
            trueBoxesFlatten.append([index, box])
    
    # Computing the number of true boxes for each image
    numBoundingBoxes = Counter([tb[0] for tb in trueBoxesFlatten])
    
    # Creating a torch.zeros tensor for each image
    for key, val in numBoundingBoxes.items():
        numBoundingBoxes[key] = torch.zeros(val)
        
    # Sorting the detections by probability of object
    predBoxFlatten.sort(key=lambda x: x[1][0], reverse=True)
    
    # Creating tensors to hold TP/FP
    TP = torch.zeros((len(predBoxFlatten)))
    FP = torch.zeros((len(predBoxFlatten)))
    totalTrueBoxes = len(trueBoxesFlatten)
    
    for detectionIndex, detection in enumerate(predBoxFlatten):
        # Getting all the true boxes for the image the detection corresponds to
        trueBoxes = [box for box in trueBoxesFlatten if box[0] == detection[0]]
        
        # Setting the best IOU
        bestIOU = 0
        
        # Iterating through each ground truth
        for index, groundTruth in enumerate(trueBoxes):
            
            # Determining the IOU between the detection and the ground truth
            # Reshaping the ground truth as the function expects 3D tensor there
            iou = IOU(detection[1], groundTruth[1].reshape((1,-1)))[0].item()
            
            # If it beats the previous best IOU, lets set it as the best IOU 
            # (i.e. this means this detection probably corresponds with this groud truth box)
            if iou > bestIOU:
                bestIOU = iou
                bestGtIndex = index
                
        # If the best IOU is greater than this index then we can set it as a true positive
        if bestIOU > iouThreshold:
            # Making sure we haven't already paired a detection with this groud truth
            # If yes, we set it as a TP
            if numBoundingBoxes[detection[0]][bestGtIndex] == 0:
                # Setting this detection as a TP
                TP[detectionIndex] = 1
                
                # Noting that this ground truth has a detection assigned to it
                numBoundingBoxes[detection[0]][bestGtIndex] = 1
            else:
                # If this ground truth already has a detection, we set it as a FP
                FP[detectionIndex] = 1
        else:
            # If this detection doesn't meet the threshold, set it as a FP
            FP[detectionIndex] = 1
        
    TP_cumsum = torch.cumsum(TP, dim=0)
    FP_cumsum = torch.cumsum(FP, dim=0)
    
    precision = TP_cumsum / (TP_cumsum + FP_cumsum)
    recalls = TP_cumsum / totalTrueBoxes
    
    precision = torch.cat(
        (torch.tensor([1]), precision))
    
    recalls = torch.cat(
        (torch.tensor([0]), recalls))
    
    return torch.trapz(precision, recalls)