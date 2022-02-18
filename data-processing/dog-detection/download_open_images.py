import fiftyone
import os

def main():
    fiftyone.config.dataset_zoo_dir = f"{os.getcwd()}"

    dataset = fiftyone.zoo.load_zoo_dataset(
                  "open-images-v6",
                  split="validation",
                  label_types=["detections","classifications"],
                  classes=["Dog"]
              )
    
    print('*********************** Completed Validation Download ***********************')

    dataset = fiftyone.zoo.load_zoo_dataset(
                  "open-images-v6",
                  split="train",
                  label_types=["detections"],
                  classes=["Dog"]
              )

    print('*********************** Completed Train Download ***********************')

    dataset = fiftyone.zoo.load_zoo_dataset(
                  "open-images-v6",
                  split="test",
                  label_types=["detections"],
                  classes=["Dog"]
              )

    print('*********************** Completed Test Download ***********************')


if __name__=='__main__':
    main()