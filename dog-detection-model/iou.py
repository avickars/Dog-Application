import numpy as np

def IOU(box, boxes):
    # box: [probObject, ymin, xmin, height, width]
    # boxes: [[probObject, ymin, xmin, height, width]...[probObject, ymin, xmin, height, width]]
    
    # Computing the Intersection
    
    # min(boxes[ymin] + boxes[height], box[ymin] + box[height]) - max(boxes[ymin], box[ymin])
    intersectionHeight = np.minimum(boxes[:,1] + boxes[:,3], box[1] + box[3]) - \
        np.maximum(boxes[:,1], box[1])
    
    
    # min(boxes[xmin] + boxes[width], box[xmin] + box[width]) - max(boxes[xmin], box[xmin])
    intersectionWidth = np.minimum(boxes[:,2] + boxes[:,4], box[2] + box[4]) - \
        np.maximum(boxes[:,2], box[2])
    
    intersection = intersectionWidth * intersectionHeight
    
    # If the intersection is negative, then they don't intersect
    intersection[intersection < 0] = 0
    
    # Computing the union
    
    # Area = height*width
    boxesArea = boxes[:,3] * boxes[:,4]
    
    # Area = height*width
    boxArea = box[3] * box[4]
    
    # Union = Area(A) + Area(B) - Intersection(AB)
    union = boxArea + boxesArea - intersection
    
    iou = intersection / union
    
    return iou