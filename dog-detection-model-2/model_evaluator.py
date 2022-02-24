from tqdm import tqdm
from params import DEVICE, CPU_DEVICE
import torch
from coco_utils import convert_to_coco_api
from coco_eval import CocoEvaluator
from mean_average_precision import MAP
from non_max_surpression import NonMaxSurpression

def evaluator(model, dataLoader):
    # Defining non max surpressor
    nms = NonMaxSurpression()

    # Getting the number of threads available
    n_threads = torch.get_num_threads()

    torch.set_num_threads(1)
    
    iou_types = ["bbox"]

    coco = convert_to_coco_api(dataLoader.dataset)
    coco_evaluator = CocoEvaluator(coco, iou_types)

    model.eval()

    # Defining loop to get the nice progress bar
    loop =  tqdm(enumerate(dataLoader), total=len(dataLoader), leave=True)

    iouTypes = ['bbox']

    outputsAll = []
    targetsAll = []

    # Turning off the gradient
    with torch.no_grad():

        # Executing each batch
        for batchIndex, (images, targets) in loop:
            # Moving everything to training device
            images = list(image.to(DEVICE) for image in images)

            outputs = model(images, targets)

            outputs = [{k: v.to(CPU_DEVICE) for k, v in t.items()} for t in outputs]

            res = {target["image_id"].item(): output for target, output in zip(targets, outputs)}

            coco_evaluator.update(res)

            # Appening outputs to calculate the MAP and execute non-max-surpression on entire validation/test set
            outputsAll += (outputs)
            targetsAll += (targets)

    coco_evaluator.accumulate()
    coco_evaluator.summarize()

    outputsAll = nms(outputsAll)
    
    APs = []
    for threshold in torch.arange(start=0.5, end=1, step=0.05):
        APs.append(MAP(outputsAll, targetsAll, threshold))
    map = sum(APs)/len(APs)

    return coco_evaluator, map

