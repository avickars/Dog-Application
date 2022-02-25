import torch
import numpy as np

class Decoder(object):
    """Decode the output of the model to match the label
    
    __init__:
        Computes the required element locations for the decoding
        Args:
            anchorBoxes (string): path to anchor box file ()
            device (pt device): tensors are using

    __call__:
        Args:
            predictions (tensor): the predictions or labels that need decoding
            inputType (string): the type of decoding

        Returns:
            returns tensor(batchSize,gridSize,gridSize,[objectProbability, ymin, xmin, height, width]*numAnchorBoxes)
    __
    
    
    """
    def __init__(self, anchorBoxes, device, gridSize=13):
        # Reading in the the anchor boxes
        with open(anchorBoxes, 'rb') as f:
            self.anchorBoxes = torch.from_numpy(np.load(f)).to(device)
            
        # Recording the number of anchor boxes
        self.numAnchorBoxes = self.anchorBoxes.shape[0]
            
        # Determining the locations of the anchor boxes in each input
        self.anchorBoxLocations = torch.arange(start=0, 
                                              end=5*self.numAnchorBoxes-1,
                                              step=5,
                                              dtype=torch.long)
        
        # Determining the locations of the xcenter in each input
        self.bYLocations = torch.arange(start=1, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        
        # Determining the locations of the ycenter in each input
        self.bXLocations = torch.arange(start=2, 
                                    end=5*self.numAnchorBoxes,
                                    step=5,
                                    dtype=torch.long)
        
        # Determining the locations of the width in each input
        self.bHLocations = torch.arange(start=3, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        
        # Determining the locations of the height in each input
        self.bWLocations = torch.arange(start=4, 
                                        end=5*self.numAnchorBoxes,
                                        step=5,
                                        dtype=torch.long)
        
        # Recording the grid size
        self.gridSize = gridSize
        
        # Creating a tensor to record which row each grid cell belongs to
        self.rowNums = torch.arange(
                0,self.gridSize,
                1
        ).reshape(
            (self.gridSize,-1)
        ).repeat(
            (1,self.numAnchorBoxes)
        ).unsqueeze(
            1
        ).repeat(
            1, 
            self.gridSize, 
            1
        ).to(device)
        
        # Creating a tensor to record which column each grid cell belongs to
        self.colNums = torch.arange(
            0,
            self.gridSize,
            1
        ).repeat(
            self.gridSize,
            1
        ).unsqueeze(
            2
        ).repeat(
            (1,1,self.numAnchorBoxes)
        ).to(device)
        
        # Recording the height/width of each anchor box
        self.anchorBoxesWidth = self.anchorBoxes[:,0]
        self.anchorBoxesHeight = self.anchorBoxes[:,1]
        
    def __call__(self, predictions, inputType='Train'):
        
        if inputType=='Train':        
            # Getting the probability of an object
            predictions[:,:,:,self.anchorBoxLocations] =  torch.sigmoid(predictions[:,:,:,self.anchorBoxLocations])

            # Getting the xcenter location relative to the entire image
            predictions[:,:,:,self.bXLocations] = torch.sigmoid(predictions[:,:,:,self.bXLocations])

            # Getting the xcenter location relative to the entire image
            predictions[:,:,:,self.bYLocations] = torch.sigmoid(predictions[:,:,:,self.bYLocations])

            # Getting the width of the predicted box
            predictions[:,:,:,self.bWLocations] = (torch.exp(predictions[:,:,:,self.bWLocations]) * \
                                                   self.anchorBoxesWidth).float()

            # Getting the height of the predicted box
            predictions[:,:,:,self.bHLocations] = (torch.exp(predictions[:,:,:,self.bHLocations]) * \
                                                   self.anchorBoxesHeight).float()
        
        # Getting the xcenter location relative to the entire image
        predictions[:,:,:,self.bXLocations] = (predictions[:,:,:,self.bXLocations]  + \
                                               self.colNums) / self.gridSize

        # Getting the xcenter location relative to the entire image
        predictions[:,:,:,self.bYLocations] = (predictions[:,:,:,self.bYLocations]  + \
                                               self.rowNums) / self.gridSize
        
        # Turning these into xcenter to xmin
        predictions[:,:,:,self.bXLocations] -= predictions[:,:,:,self.bWLocations]/2
        
        # Turning these from ycenter to ymin
        predictions[:,:,:,self.bYLocations] -= predictions[:,:,:,self.bHLocations]/2

        # Some of the predictions can be slightly negative, and possibly greater than 1, so just clamping them.
        predictions = torch.clamp(predictions, min=0, max=1)


        
        
        

        return predictions.cpu()