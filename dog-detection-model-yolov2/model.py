from torch import nn
from torchvision import models
import torch

def space_to_depth(x, block_size):
    # CITATION: https://stackoverflow.com/questions/58857720/is-there-an-equivalent-pytorch-function-for-tf-nn-space-to-depth
    n, c, h, w = x.size()
    unfolded_x = torch.nn.functional.unfold(x, block_size, stride=block_size)
    return unfolded_x.view(n, c * block_size ** 2, h // block_size, w // block_size)

class DogDetectorModel(nn.Module):
    def __init__(self, modelPath=None, gridSize=13, numAnchorBoxes=7):
        super(DogDetectorModel, self).__init__()
        
        # Recording the grid size
        self.gridSize = 13
        
        # Recording the number of anchor boxes
        self.numAnchorBoxes = numAnchorBoxes
        
        # Reading in the pre-trained feature extractor
        self.featureExtractor = models.vgg19_bn(pretrained=True).features
        
        # Freezing the weights of the pre-trained feature extractor
        for parameter in self.featureExtractor.parameters():
            parameter.requires_grad = False
            
        # Defining the object detection layers
        # These layers follow right up to the line in Table 6 (Darknet-19) in YoloV2 Paper
        self.objectDetectorPart1 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),
            
            nn.Conv2d(in_channels=1024, out_channels=512, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),
            
            nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),        
            
            nn.Conv2d(in_channels=1024, out_channels=512, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),
            
            nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1)
        )
        
        # Additional 2 of 3 layers
        self.objectDetectorPart2 = nn.Sequential(
            nn.Conv2d(in_channels=1024, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),
            
            nn.Conv2d(in_channels=1024, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1)
        )
        
        # Additional 3 of 3 layers (for after skip connection)
        self.objectDetectorPart3 = nn.Sequential(
            nn.Conv2d(in_channels=3072, out_channels=1024, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.LeakyReLU(0.1),
        )
        
        # Adding output layer 
        self.output = nn.Sequential (
            nn.Conv2d(in_channels=1024, out_channels=numAnchorBoxes*5, kernel_size=1, stride=1, padding=0, bias=True)
        )    
        
       
    def forward(self, modelInput):
        # Not Executing the MaxPool that is at #52 yet, need to record the skip connection
        tmp = self.featureExtractor[0:52](modelInput)   
        
        # Recording the high resolution features
        skipConnection = tmp
            
        # Concatting the high/low res features (changes from 512*26*26 -> 2048*13*13)
        skipConnection = space_to_depth(skipConnection, 2)
        
        # Executing the MaxPool at #52
        tmp = self.featureExtractor[52](tmp)  
        
        # Executing the 1st part of the object detector
        tmp = self.objectDetectorPart1(tmp)
        
        # Executing the 2nd part of the object detector
        tmp = self.objectDetectorPart2(tmp)
        
        # Concatenating with the skip connection
        tmp = torch.cat([tmp, skipConnection],dim=1)
        
        # Executing the 3rd part of the object detector
        tmp = self.objectDetectorPart3(tmp)  
        
        # Computing the output (i.e. final conv layer with correct dimensions)
        tmp = self.output(tmp)  
        
        # Reshaping to match the label
        tmp = tmp.reshape((-1, self.gridSize, self.gridSize, 5*self.numAnchorBoxes))
        
        # Returning the model output
        return tmp