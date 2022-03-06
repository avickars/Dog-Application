import torch

def l2(v1, v2):
    return torch.sqrt(
        torch.sum(
            torch.square(v1-v2) ,
            dim=1)
    )

def sigmoidL2(v1, v2):
    return torch.sigmoid(
        l2(v1, v2)
    )