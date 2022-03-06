import torch

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

IMAGE_SIZE = 448

CPU_DEVICE = torch.device("cpu")

MARGIN = 0.9