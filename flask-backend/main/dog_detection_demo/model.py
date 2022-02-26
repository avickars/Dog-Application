from torch import nn
from torchvision import models
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

class DogDetectorModel(nn.Module):
    # CITATION: https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
    
    def __init__(self, modelPath=None):
        super(DogDetectorModel, self).__init__()
        # We only have 2 classes (dog and background)
        numClasses = 2
        
        # load a model pre-trained on COCO
        self.model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        
        # get number of input features for the classifier
        inFeatures = self.model.roi_heads.box_predictor.cls_score.in_features
        
        # Rejigging the output to have the correct number of classifying features
        self.model.roi_heads.box_predictor = FastRCNNPredictor(inFeatures, numClasses)

    def forward(self, image, label):
        if self.model.training:
            # Returning the training model output
            return self.model(image, label)
        else:
            return self.model(image)
