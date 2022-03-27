# dog-identification-model

## Requirements
- torch 1.11.0
- torchvision 0.12.0
- pandas 1.4.1
- PIL 8.4.0
- tqdm 4.62.3
- matplotlib 3.5.1
- numpy 1.21.2
- scikit-learn 1.0.2

## Data

All data that is created/used is located here: https://1sfu-my.sharepoint.com/:f:/g/personal/avickars_sfu_ca/EiTssrkV8qROmeNQSJxK3SAB79aOBMwO1dpDdpCSpQ9X3A?e=m7s1ID

## data_cleaning.ipynb

This notebook cleans the Pet Finder data set, and determines the bounding box of every dog in every image.  Images that contain multiple dogs or no dogs are removed.  
This notebook creates the attributes.csv, & boxesDF.csv files.

## data_dividation.ipynb

This notebook splits the data into a training, validation and test splits.

## breed_extraction.ipynb

This notebook parses the breeds of every dog into a uniform format using the breeds from the Stanford Dogs Dataset as the master list of breeds.  This noteboke outputs the attributes_breed.csv file.

## data_loader_test.py

This is a data loader for the model with a cross entropy loss. Every batch element is two images of the same dog, or two images of different dogs.

## data_loader_test_breed.py

This is a data loader for the model with a cross entropy loss. Every batch element is two images of the same dog, or two images of different dogs that are of the same breed.

## data_loader_train.py

This is a data loader for the model with a triplet loss. Every batch element is a positive, anchor and negative image.

## data_loader_train_breed.py

This is a data loader for the model with a triplet loss. Every batch element is a positive, anchor and negative image where all images are of dogs of the same breed.

## data_loader_pipeline.py

This data loader just returns two images of the indexed dog.  Used in pipeline_testing.ipynb

## data_transformations.py

This script contains the declaration of the transforms applied to every image during the model training and testing process.

## loss.py

This script contains the declaration of both the cross entropy and triplet loss functions.  Also contains the sigmoid L2 distance function that is used frequently.

## iou.py

Contains declaration of the intersection over union function.

## image_to_tensor.py

Contains function that converts a list of image paths to a tensor

## model.py

Contains the declaration of the dog-identification model.

## model_dog_detection.py

Contains the declaration of the dog detection model to use when loading the model.

## model_evaluator.py

Contains function used to evaluate the model.  Can be used for both triplet and cross entropy loss by uncommenting lines as needed.  Currently, in cross entropy loss form.

## model_testing.ipynb

This notebook contains the testing results applied on the dog-identification model.  It:
- Plots the model training curves
- Determines the optimum classification threshold to use over the validation data.
- Computes the classification and f1 scores on either the validation or test data (using the optimum classfication threshold)

## model_trainer.py

Contains the function used to train the dog-identification model.  Currently, in cross entropy loss form.

## model_training.ipynb

This notebook trains the dog-identification model.  It is used to train the model using both a triplet loss and cross entropy loss (currently set to use cross entropy loss)

## model_training_further.ipynb

This notebook applied additional training ton the dog-identification model by using the breed data loader that when generating two images of different dogs, the dogs are of the same breed.\

## non_max_surpression.py

Contains implementation of non max suppression algorithm

## params.py

Contains declaration of various parameters used.

## pipeline_testing.ipynb

This notebook determines the optimum parameters to use in the pipeline between all three models.  It then uses these parameters and applies them over the test and validation accuracy to determine how well the pipeline matches lost and found dogs.

## data_dividation.ipynb

This notebook divides the petfinder data set into training, validation and test splits.
