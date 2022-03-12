# Loading in functions
from main.dog_detection_demo.non_max_surpression import NonMaxSurpression
from main.dog_detection_demo.model import DogDetectorModel
from main.dog_detection_demo.image_to_tensor import to_tensor
import os
# Loading libraries
import torch


def dog_extractor(image):

	cwd = os.getcwd()

	cwd = cwd +  '/dog_detection_demo/model.pt'

	# Initializing the model
	model = DogDetectorModel()

	# Initializing Non Max Surpression with default parameters
	nms = NonMaxSurpression()

	# Loading the checkpoint
	checkpoint = torch.load(cwd, map_location=torch.device('cpu')) 

	# Loading the model weights
	model.load_state_dict(checkpoint['model_state_dict'])

	# Setting model to evaluation model
	model = model.eval()

	# Loading and transforming images
	images = to_tensor([image])

	# Running image through model
	outputs = model(images, '')

	# Executing non max surpression on the model output
	outputs = nms(outputs)

	return outputs
