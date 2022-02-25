import numpy as np

def iou_yolo(box, boxes):
    # CITATION: https://fairyonice.github.io/Part_1_Object_Detection_with_Yolo_for_VOC_2014_data_anchor_box_clustering.html 
    # box: [width, height]
    # boxes: [[width, height]...[width, height]]
    
    # Computing the intersection
    intersectionWidth = np.minimum(box[0],boxes[:,0])
    intersectionHeight = np.minimum(box[1],boxes[:,1])
    intersection = intersectionWidth * intersectionHeight
    
    # Area = Length * Width
    boxArea = box[0] * box[1]
    
    boxesArea = boxes[:,0] * boxes[:,1]
    
    # Union = Area(A) + Area(B) - Intersection(AB)
    union = boxArea + boxesArea - intersection
    
    iou = intersection / union
    
    return iou