from collections import Counter
from iou import IOU
import torch

def MAP(output, truth, iouThreshold=0.05):
    # CITATION: https://www.youtube.com/watch?v=FppOzcDvaDI&t=1289s
    
    # Iterating through all the results and merging them into a list
    predBoxes = []
    for i in range(0,len(output)):
        for j in range(0, output[i]['boxes'].shape[0]):
            predBoxes.append([i] + [output[i]['scores'][j].item()] + output[i]['boxes'][j].tolist())
    
    # Iterating through all the truths and merging them into a list
    trueBoxes = []
    for i in range(0,len(truth)):
        for j in range(0, truth[i]['boxes'].shape[0]):
            trueBoxes.append([i] + truth[i]['boxes'][j].tolist())
    
    # Counts the number of true boxes in each image
    numBoxesPerImage = Counter([gt[0] for gt in trueBoxes])
    
    for key, val in numBoxesPerImage.items():
        numBoxesPerImage[key] = torch.zeros(val)
        
    # Sorting the boxes by confidence
    predBoxes.sort(key=lambda x: x[1], reverse=True)
    
    # Defining tensors to hold TP and FP indicator
    TP = torch.zeros((len(predBoxes)))
    FP = torch.zeros((len(predBoxes)))
    
    # Iterating through each detection
    for detectionIndex, detection in enumerate(predBoxes):
        
        # Extracting the true boxes that are from the image with this detection
        groundTruthBoxes = [bbox for bbox in trueBoxes if bbox[0] == detection[0]]
        
        # Defining best IOU
        bestIOU = 0
        
        # Defining the number of true boxes
        numTrueBoxes = len(groundTruthBoxes)
        
        # Iterating through the groundTruthBoxes to check the IOU
        for truthIndex, trueBox in enumerate(groundTruthBoxes):
            iou = IOU(torch.tensor(trueBox), torch.tensor(detection)[1:].reshape((1,-1)))
            
            # If it is the best IOU for this box, we record it
            if iou > bestIOU:
                bestIOU = iou
                bestIOUIndex = truthIndex
        
        # if this bestIOU is greater than the threshold (or not) we record it accordingly
        if bestIOU > iouThreshold:
            if numBoxesPerImage[detection[0]][bestIOUIndex] == 0:
                numBoxesPerImage[detection[0]][bestIOUIndex] = 1
                TP[detectionIndex] = 1
            else:
                FP[detectionIndex] = 1
        else:
            FP[detectionIndex] = 1

    TP_cumSum = torch.cumsum(TP, dim=0)
    FP_cumSum = torch.cumsum(FP, dim=0)
    
    precisions = torch.divide(TP_cumSum, TP_cumSum + FP_cumSum)
    recall = torch.divide(TP_cumSum, len(trueBoxes))
    
    
    precisions = torch.cat((torch.tensor([1]), precisions))
    recall = torch.cat((torch.tensor([0]), recall))
    
    ap = torch.trapezoid(precisions, recall)
    
    return ap
