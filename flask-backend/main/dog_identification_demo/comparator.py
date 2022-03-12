# Loading in functions
from main.dog_identification_demo.transforms import load_and_transform
from main.dog_identification_demo.model import DogIdentificationModel
from main.dog_identification_demo.sigmoidL2 import sigmoidL2
# Loading libraries
import os
import torch


def dog_comparator(image, bounding_boxes):

	cwd = os.getcwd()

	cwd = cwd +  '/dog_identification_demo/dog-identification-model.pt'

	# Load and Transform image
	images = load_and_transform([image], bounding_boxes)

	# Initializing the model
	model = DogIdentificationModel()

	# Loading the checkpoint
	checkpoint = torch.load(cwd, map_location=torch.device('cpu'))

	# Loading the model weights
	model.load_state_dict(checkpoint['model_state_dict'])

	# Passing it to model
	outputs = model(images)

	# Converting tensor to list
	outputs = outputs.tolist()

	return outputs


def sigmoid(box1, box2):
	comparison = sigmoidL2(box1, box2)
	return comparison
