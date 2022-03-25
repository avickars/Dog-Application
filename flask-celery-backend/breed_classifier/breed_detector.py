import os
import torch
from torch import nn
from PIL import Image
from torchvision import transforms
from torch.autograd import Variable
import torchvision.models as models


def predict_breed(filename):
    cwd = os.getcwd()
    breeds_file = cwd + '/breed_classifier/stanford_dogs_breeds_classes_final.txt'
    cwd = cwd + '/breed_classifier/vgg19_60_based_model2.pt'
    model_vgg19 = models.vgg19(pretrained=True)

    for param in model_vgg19.parameters():
        param.requires_grad = False

    model_vgg19.classifier = nn.Sequential(*list(model_vgg19.classifier.children())[:-1] + [nn.Linear(in_features=4096, out_features=120, bias=True)])

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_vgg19 = model_vgg19.to(device)
    model_vgg19.load_state_dict(torch.load(cwd, map_location=torch.device('cpu')), strict=False)
    model_vgg19.eval()

    input_image = Image.open(filename)

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

    with open(breeds_file, "r") as f:
        categories = [s.strip() for s in f.readlines()]

    predicted_breeds = []
    top3_prob, top3_catid = torch.topk(probabilities, 5)
    for i in range(top3_prob.size(0)):
        predicted_breeds.append(categories[top3_catid[i]])

    return predicted_breeds
