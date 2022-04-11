# Dog-Application/model2-breed_classification

	This directory contains all the files related to Breed Classifier Models.

## jupyter_notebooks/             

	This folder contains all the python notebook files
	used to build different models for dog breed classification.

## colab_notebooks/

	This folder contains templates for collab notebooks to train
	a pretrained  model in Google Collab.

## pretrained-model-comparisons.csv, pretrained-model-comparisons.xlsx         

	These files have the Acc@1 and Acc@5 scores of pretrained PyTorch models on ImageNet.
	The data was downloaded from :
		https://pytorch.org/vision/stable/models.html

## predict_dog_breed_model2.py

	This file uses the final VGG19 based Breed Classification model to predict
	a dog's breed and outputs the top 3 possible breeds with their probabilities.

	This file was directly used in the pipeline.

## model2-comparisons.csv and model2-comparisons.xlsx        

	These files contain the train, validation, and testing data such as
	training time, validation loss and accuracy, testing loss and accuracy,
	precision, recall, F1 scores etc for various models trained in
	colab_notebooks folder.

## visualize-compare-models.ipynb, val_accuracy_comp_fig.png and test_accuracy_comp_fig.png

	These visualizes the validation loss, validation accuracy, testing loss and
	testing accuracies of various models.
	model2-comparisons.csv data file was used a source for visualizations.  

## dog.jpg                                

	 This photo is being used a test dog photo in predict_dog_breed_model2.py.
	 This image was downloaded from:
	 	https://a-z-animals.com/media/animals/images/original/labrador_retriever.jpg

## drive_link_to_pt_files_of_model2.txt   
	This file contains a google drive link where all the .pt files
	of trained models can be downloaded from.

## stanford_dogs_breeds_sorted.txt, stanford_dogs_breeds.txt, stanford_dogs_breeds_classes_final.txt

	These files contain names of 120 breeds of stanford dataset.
	
