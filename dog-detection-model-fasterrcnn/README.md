# dog-detection-model-fasterrcnn

## Requirements
- torch 1.11.0
- torchvision 0.12.0
- pandas 1.4.1
- PIL 8.4.0
- tqdm 4.62.3
- matplotlib 3.5.1
- numpy 1.21.2

## Data

All data that is created/used is located here: https://1sfu-my.sharepoint.com/:f:/g/personal/avickars_sfu_ca/Ek3xx9eaoldDkMVHBB_CTZ0BlFbXx1j_omyxPf2h690LIw?e=URHmrZ

## coco_eval.py/coco_utils.py/model_utils.py

Contain declarations of various utilities used in model training/testing process.

## data_loader.py

Contains the data loader used in model training/testing

## params.py

Contains the declarations of parameters used in model training/testing

## non_max_surpression.py

Contains non max surpression algorithm implementation

## mean_average_precision.py

Contains mean average precision algorithm implementation

## model_trainer.py

Contains the function used to train the model.  It is called from model_training.ipynb

## model_tester.py

Contains the function used to test the model.  It is called from model_training.ipynb

## model.py

Contains the declaration of the model used

## iou.py

Contains the implementation of the intersection over union.  It is called in non max surpression.

## model_testing.ipynb

Determines the optimum cutoffs to use in NMS, and tests on test and validation data

## model_training.ipyng

Trainings the model.


