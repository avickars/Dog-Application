def true_box_extractor(label, decodedLabel):
    # Defining lists to hold the boxes for this batch set
    trueBoxes = []

    # Iterating through each element in the batch
    for batchElement in range(0,label.shape[0]):
        
        # Defining list to hold labels for this batch element
        boxes = []
        
        # Starting counter
        i = 0
        
        # Getting the box locations in the label
        boxLocations = label[batchElement].nonzero()

        while i < boxLocations.shape[0] // 5:
            boxes.append(
                decodedLabel[
                    batchElement, 
                    boxLocations[i*5][0].item(),
                    boxLocations[i*5][1].item(), 
                    boxLocations[i*5][2].item():boxLocations[i*5][2].item()+5
                ]
            )
            i += 1
        
        trueBoxes.append(boxes)

    return trueBoxes