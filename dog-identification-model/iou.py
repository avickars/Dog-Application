import torch

def IOU(box, boxes):
    # box: [probObject, xmin, ymin, xmax, ymax]
    # boxes: [[probObject, xmin, ymin, xmax, ymax]...[probObject, xmin, ymin, xmax, ymax]]
    
    # Computing the Intersection

    intersectionWidth = torch.maximum(boxes[:,1], box[1]) - torch.minimum(boxes[:,3], box[3]) 
    
    intersectionHeight = torch.maximum(boxes[:,2], box[2]) - torch.minimum(boxes[:,4], box[4]) 
    
    intersection = intersectionWidth * intersectionHeight
    
    # If the intersection is negative, then they don't intersect
    intersection[intersection < 0] = 0
    
    # Computing the union
    
    # Area = height*width
    boxesArea = (boxes[:,3] - boxes[:,1]) * (boxes[:,4] - boxes[:,2])
    
    # Area = height*width
    boxArea = (box[3] - box[1]) * (box[4] - box[2])
    
    # Union = Area(A) + Area(B) - Intersection(AB)
    union = boxArea + boxesArea - intersection
    
    iou = intersection / union
    
    return iou