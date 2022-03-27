from tqdm import tqdm
from params import DEVICE
import math
import sys
from loss import triplet_loss,cross_entropy_loss
from params import MARGIN


def trainer(model, optimizer, dataLoader, epoch):
    model.train()

    # Defining loop to get the nice progress bar
    loop = tqdm(enumerate(dataLoader), total=len(dataLoader), leave=True)

    allLosses = []

    numObservations = 0

    # Executing each batch
    # for batchIndex, (index, negativeImgIndex, positiveImg, anchorImg, negativeImg) in loop:
    for batchIndex, (negativeImg, positiveImg, label) in loop:
        # Moving everything to training device
        positiveImg = positiveImg.to(DEVICE)
        # anchorImg = anchorImg.to(DEVICE)
        negativeImg = negativeImg.to(DEVICE)

        # label = label.to(DEVICE)

        # zero the parameter gradients
        optimizer.zero_grad()

        # Computing the model output
        positiveImgEncoding = model(positiveImg)
        # anchorImgEncoding = model(anchorImg)
        negativeImgEncoding = model(negativeImg)

        # Summing to total the loss of all types
        # lossTotal = triplet_loss(anchorImgEncoding, positiveImgEncoding, negativeImgEncoding, MARGIN)
        lossTotal = cross_entropy_loss(positiveImgEncoding, negativeImgEncoding, label)

        # Extracting the loss to use in case it goes to nan
        loss = lossTotal.item()
        if not math.isfinite(loss):
            print(f"Loss is {loss}, stopping training")
            sys.exit(1)

        # Backpropating the loss
        lossTotal.backward()

        # Updating the weights
        optimizer.step()

        # Outputting the loss
        loop.set_description(f"EPOCH: {epoch} | Loss {loss / positiveImg.shape[0]}")

        allLosses.append(loss)

        numObservations += positiveImg.shape[0]

    meanLoss = sum(allLosses) / numObservations

    print(f"EPOCH: {epoch} | Final Training Mean Loss {meanLoss}")

    return meanLoss