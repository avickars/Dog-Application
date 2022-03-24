#!/usr/bin/env python
# coding: utf-8

# this script has been transformed from testing_vgg19_60ep_model2.ipynb notebook

import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import torchvision.models as models
from torchvision.datasets import ImageFolder
from IPython.display import Image
from PIL import Image
from torchvision import transforms
from torchvision.transforms import ToTensor

from torch.autograd import Variable


# ## load the Vgg19 based model

model_vgg19 = models.vgg19(pretrained=True)

for param in model_vgg19.parameters():
    param.requires_grad = False

model_vgg19.classifier = nn.Sequential(*list(model_vgg19.classifier.children())[:-1] + [nn.Linear(in_features=4096, out_features=120, bias=True)])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model_vgg19 = model_vgg19.to(device)

model_vgg19.load_state_dict(torch.load('vgg19_60_based_model2.pt'), strict=False)
model_vgg19.eval()

# ref for dog image: https://a-z-animals.com/media/animals/images/original/labrador_retriever.jpg
filename = 'dog.jpg' #labrador
input_image = Image.open(filename)

# preprocess the image for the model
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
    )
])

input_tensor = preprocess(input_image)
if torch.cuda.is_available():
    input_tensor = Variable(input_tensor.cuda())

input_batch = input_tensor.unsqueeze(0)
out = model_vgg19(input_batch)

probabilities = torch.nn.functional.softmax(out[0], dim=0)
# print(probabilities)

with open("stanford_dogs_breeds_classes_final.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

predicted_breeds = []
top3_prob, top3_catid = torch.topk(probabilities, 3)
for i in range(top3_prob.size(0)):
    # print('Predicted breed:', categories[top3_catid[i]], top3_prob[i].item()*100)
    predicted_breeds.append((categories[top3_catid[i]], top3_prob[i].item()*100))

# list to be used directly by the application (predicted_breed, probability)
print("predicted_breeds are: \n", predicted_breeds)
