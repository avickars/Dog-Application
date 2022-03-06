from tqdm import tqdm
from params import DEVICE
import torch
from triplet_loss import triplet_loss
from params import MARGIN


def evaluator(model, dataLoader, epoch):

    model.eval()

    # Defining loop to get the nice progress bar
    loop = tqdm(enumerate(dataLoader), total=len(dataLoader), leave=True)

    allLosses = []

    numObservations = 0

    # Turning off the gradient
    with torch.no_grad():

        # Executing each batch
        for batchIndex, (index, negativeImgIndex, positiveImg, anchorImg, negativeImg) in loop:
            # Moving everything to training device
            positiveImg = positiveImg.to(DEVICE)
            anchorImg = anchorImg.to(DEVICE)
            negativeImg = negativeImg.to(DEVICE)

            # Computing the model output
            positiveImgEncoding = model(positiveImg)
            anchorImgEncoding = model(anchorImg)
            negativeImgEncoding = model(negativeImg)

            # Summing to total the loss of all types
            lossTotal = triplet_loss(anchorImgEncoding, positiveImgEncoding, negativeImgEncoding, MARGIN)

            allLosses.append(lossTotal.item())

            # Outputting the loss
            loop.set_description(f"EPOCH: {epoch} | Loss {lossTotal.item() / positiveImg.shape[0]}")

            numObservations += positiveImg.shape[0]

    meanLoss = sum(allLosses) / numObservations

    print(f"EPOCH: {epoch} | Final Validation Mean Loss {meanLoss}")

    return meanLoss

