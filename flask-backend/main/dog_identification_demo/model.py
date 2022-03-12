from torch import nn
from torchvision import models


class DogIdentificationModel(nn.Module):

    def __init__(self, modelPath=None):
        super(DogIdentificationModel, self).__init__()

        # load a model pre-trained on COCO
        self.model = models.vgg19_bn(pretrained=True)

        self.model.classifier = self.model.classifier = nn.Sequential(
            nn.Linear(25088, 500),
            nn.ReLU(),
            nn.Linear(500, 500),
            nn.ReLU(),
            nn.Linear(500, 5)
        )

    def forward(self, image):
        return self.model(image)