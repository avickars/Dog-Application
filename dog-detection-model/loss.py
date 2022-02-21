import torch
from torch import nn
import numpy as np

class YoloLoss(nn.Module):
    def __init__(self, anchorBoxes, device, lambdaCoord=5, lambdaNoObj=0.5, gridSize=13, numAnchorBoxes=7):
        super().__init__()
        self.lambdaCoord = lambdaCoord
        self.lambdaNoObj = lambdaNoObj
        self.gridSize = gridSize
        self.numAnchorBoxes = numAnchorBoxes
        
        self.anchorBoxLocations = torch.arange(start=0, 
                                              end=5*self.numAnchorBoxes-1,
                                              step=5,
                                              dtype=torch.long)
        self.bXLocations = torch.arange(start=1, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        self.bYLocations = torch.arange(start=2, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        self.bWLocations = torch.arange(start=3, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        self.bHLocations = torch.arange(start=4, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        
        # Reading in the the anchor boxes
        with open(anchorBoxes, 'rb') as f:
            self.anchorBoxes = torch.from_numpy(np.load(f)).to(device)
            
        self.anchorBoxesWidth = self.anchorBoxes[:,0]
        self.anchorBoxesHeight = self.anchorBoxes[:,1]
        
        
    def forward(self, predictions, target):
        
        probObjectAndIou_hat =  torch.sigmoid(predictions[:,:,:,self.anchorBoxLocations])
        probObjectAndIou = target[:,:,:,self.anchorBoxLocations]
        probNoObjectAndIou = 1-target[:,:,:,self.anchorBoxLocations]
        
        bX_hat = torch.sigmoid(predictions[:,:,:,self.bXLocations])
        bX = target[:,:,:,self.bXLocations]
        
        bY_hat = torch.sigmoid(predictions[:,:,:,self.bYLocations])
        bY = target[:,:,:,self.bYLocations]
        
        bW_hat = torch.exp(predictions[:,:,:,self.bWLocations]) * self.anchorBoxesWidth
        bW = target[:,:,:,self.bWLocations]
        
        bH_hat = torch.exp(predictions[:,:,:,self.bHLocations]) * self.anchorBoxesHeight
        bH = target[:,:,:,self.bHLocations]
        
        # ********* BOX LOSS *********
        
        # Computing the square differences between the predicted and real x/y coordinates
        xLoss = torch.square(bX - bX_hat)
        yLoss = torch.square(bY - bY_hat)
    
        # Putting them together and applying filter (i.e. only the gridcell/anchor box that is
        # responsible takes any loss)
        xyLoss = self.lambdaCoord * torch.sum(probObjectAndIou * (xLoss + yLoss))
        
        # Computing the square differences between the predicted and real h/w values
        wLoss = torch.square(torch.sqrt(bW) - torch.sqrt(bW_hat))
        hLoss = torch.square(torch.sqrt(bH) - torch.sqrt(bH_hat))
    
        # Putting them together and applying filter (i.e. only the gridcell/anchor box that is
        # responsible takes any loss)
        hwLoss = self.lambdaCoord * torch.sum(probObjectAndIou * (wLoss + hLoss))
        
        # ********* Object LOSS *********
        objectLoss = torch.sum(probObjectAndIou * torch.square(probObjectAndIou - probObjectAndIou_hat))
        
        noObjectLoss = self.lambdaNoObj * torch.sum(probNoObjectAndIou * torch.square(probObjectAndIou - probObjectAndIou_hat))
        
        loss = xyLoss + hwLoss + objectLoss + noObjectLoss
        
        return loss