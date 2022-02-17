import numpy as np

def IOU(box, boxes):
    # box: [x_min, x_max, y_min, y_max]
    # boxes: [[x_min, x_max, y_min, y_max]...[x_min, x_max, y_min, y_max]]
    
    # Computing the Intersection
    intersectionWidth = np.minimum(boxes[:,1], box[1]) - np.maximum(boxes[:,0], box[0])
    intersectionHeight = np.minimum(boxes[:,3], box[3]) - np.maximum(boxes[:,2], box[2])
    intersection = intersectionWidth * intersectionHeight
    
    # If the intersection is negative, then they don't intersect
    intersection[intersection < 0] = 0
    
    # [x_min, y_min]
    minHeightAndWidth = boxes[:, [0,2]]
    
    # [x_max, y_max]
    maxHeightAndWidth = boxes[:, [1,3]]
    
    # [width, height]
    widthAndHeight = maxHeightAndWidth - minHeightAndWidth
    
    # Area = width * height
    boxesArea = widthAndHeight[:,0] * widthAndHeight[:,1]
    
    # Area = (x_max - x_min)*(y_max-y_min)
    boxArea = (box[1] - box[0])*(box[3] - box[2])
    
    # Union = Area(A) + Area(B) - Intersection(AB)
    union = boxArea + boxesArea - intersection
    
    iou = intersection / union
    
    return iou