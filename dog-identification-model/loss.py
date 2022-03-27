import torch

sig = torch.nn.Sigmoid()
relu = torch.nn.Sigmoid()

crossEntropy = torch.nn.BCELoss()

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

def triplet_loss(anchorOutput, positiveOutput, negativeOutput, margin):
    d1 = sigmoidL2(anchorOutput,positiveOutput)

    d2 = sigmoidL2(negativeOutput, anchorOutput)

    loss = relu(d1 - d2 + margin)

    totalLoss = torch.sum(loss)

    return totalLoss

def cross_entropy_loss(img1, img2, label):
    distance = sigmoidL2(img1,img2)

    label = label.reshape(label.shape[0])

    loss = crossEntropy(distance, label)


    return loss

