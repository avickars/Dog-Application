from tqdm import tqdm
from params import DEVICE
import math
import sys
import torch
from triplet_loss import triplet_loss


def trainer(model, optimizer, dataLoader, epoch):
    model.train()

    # Defining loop to get the nice progress bar
    loop = tqdm(enumerate(dataLoader), total=len(dataLoader), leave=True)

    # lr_scheduler = None
    # if epoch == 0:
    #     warmup_factor = 1.0 / 1000
    #     warmup_iters = min(1000, len(dataLoader) - 1)
    #
    #     lr_scheduler = torch.optim.lr_scheduler.LinearLR(
    #         optimizer, start_factor=warmup_factor, total_iters=warmup_iters
    #     )

    allLosses = []

    # Executing each batch
    for batchIndex, (positiveImg, anchorImg, negativeImg) in loop:
        # Moving everything to training device
        positiveImg = positiveImg.to(DEVICE)
        anchorImg = anchorImg.to(DEVICE)
        negativeImg = negativeImg.to(DEVICE)

        # zero the parameter gradients
        optimizer.zero_grad()

        # Computing the model output
        positiveImgEncoding = model(positiveImg)
        anchorImgEncoding = model(anchorImg)
        negativeImgEncoding = model(negativeImg)

        # Summing to total the loss of all types
        lossTotal = triplet_loss(anchorImgEncoding, positiveImgEncoding, negativeImgEncoding, 0.2)

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
        loop.set_description(
            f"EPOCH: {epoch} | Loss {loss}")

        # if lr_scheduler is not None:
        #     lr_scheduler.step()

        allLosses.append(loss)

    meanLoss = sum(allLosses) / len(allLosses)

    loop.set_description(
        f"EPOCH: {epoch} | Mean Loss {meanLoss}")