from tqdm import tqdm
from params import DEVICE
import math
import sys
import torch

def trainer(model, optimizer, dataLoader, epoch):
    model.train()

    # Defining loop to get the nice progress bar
    loop =  tqdm(enumerate(dataLoader), total=len(dataLoader), leave=True)


    lr_scheduler = None
    if epoch == 0:
        warmup_factor = 1.0 / 1000
        warmup_iters = min(1000, len(dataLoader) - 1)

        lr_scheduler = torch.optim.lr_scheduler.LinearLR(
            optimizer, start_factor=warmup_factor, total_iters=warmup_iters
        )

    # Executing each batch
    for batchIndex, (images, targets) in loop:
        # Moving everything to training device
        images = list(image.to(DEVICE) for image in images)
        targets = [{k: v.to(DEVICE) for k, v in t.items()} for t in targets]

        # zero the parameter gradients
        optimizer.zero_grad()

        # Computing the model output
        lossDict = model(images, targets)
        
        # Summing to total the loss of all types
        losses = sum(loss for loss in lossDict.values())
        
        # Extracting the loss to use in case it goes to nan
        loss = losses.item()
        if not math.isfinite(loss):
            print(f"Loss is {loss}, stopping training")
            sys.exit(1)
            
        # Backpropating the loss
        losses.backward()
        
        # Updating the weights
        optimizer.step()

        # Outputting the loss
        loop.set_description(f"EPOCH: {epoch} | Classifier Loss {lossDict['loss_classifier']} | Bbox Loss: {lossDict['loss_box_reg']} | Objectness Loss {lossDict['loss_objectness']} | Loss {loss}")

        if lr_scheduler is not None:
            lr_scheduler.step()