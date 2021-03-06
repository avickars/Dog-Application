import torch

# Defining the batch size to use during training
BATCH_SIZE = 30

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

IMAGE_SIZE = 448

CPU_DEVICE = torch.device("cpu")