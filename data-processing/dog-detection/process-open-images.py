import pandas as pd
import os
import PIL.Image

def main():
    for type in ['test', 'train', 'validation']:
        # Removing Non Dog Boxes
        detections = pd.read_csv(f"open-images-v6/{type}/labels/detections.csv", index_col=0)
        detections = detections[detections['LabelName'] == '/m/0bt9lr']

        # Determining Image height and Wight
        imageRowWidth = []
        for image in os.listdir(f"open-images-v6/{type}/data"):

            # Reading in the image
            img = PIL.Image.open(f"open-images-v6/{type}/data/{image}")

            # Determining the actual height and width
            w, h = img.size

            # Recording the height and width
            imageRowWidth.append([image[0:-4], w, h])

        # Creating dataframe
        rowWidthDf = pd.DataFrame(imageRowWidth, columns=['ImageID', 'imageWidth','imageHeight'])
        
        # Merging with detections
        appendedDetections = pd.merge(detections, rowWidthDf)


        appendedDetections.to_csv(f"open-images-v6/{type}/labels/detections.csv")    






if __name__=='__main__':
    main()
