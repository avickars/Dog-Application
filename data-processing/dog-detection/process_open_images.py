import pandas as pd
import os
import PIL.Image

def main():
    for type in ['test', 'train', 'validation']:
            # Removing Non Dog Boxes
            detections = pd.read_csv(f"open-images-v6/{type}/labels/detections.csv")
            detections = detections[detections['LabelName'] == '/m/0bt9lr']

            # Determining Image height and Wight
            imageRowWidth = []
            for image in os.listdir(f"open-images-v6/{type}/data"):

                # Reading in the image
                img = PIL.Image.open(f"open-images-v6/{type}/data/{image}")
                
                # Computing the image ID
                imageID = image[0:-4]
                
                # If the image is greyscale
                if img.mode == 'L':
                    
                    # Deleting the image
                    os.remove(f"open-images-v6/{type}/data/{image}")

                    # Removing it from our list
                    detections = detections[~(detections['ImageID'] == imageID)]
                    
                    continue
                    
                # If the image has a different type, we convert to RGB
                elif img.mode == 'CMYK':
                    
                    # Converting to RGB
                    img = img.convert('RGB')
                    
                    # Overwriting
                    img.save(f"open-images-v6/{type}/data/{image}")
                

                # Determining the actual height and width
                w, h = img.size

                # Recording the height and width
                imageRowWidth.append([imageID, w, h])
                
            # Creating dataframe
            rowWidthDf = pd.DataFrame(imageRowWidth, columns=['ImageID', 'imageWidth','imageHeight'])
            
            # Merging with detections
            appendedDetections = pd.merge(detections, rowWidthDf)

            # Converting the box coordinates
            appendedDetections['XMin'] = appendedDetections['XMin'] * appendedDetections['imageWidth']
            appendedDetections['XMax'] = appendedDetections['XMax'] * appendedDetections['imageWidth']
            appendedDetections['YMin'] = appendedDetections['YMin'] * appendedDetections['imageHeight']
            appendedDetections['YMax'] = appendedDetections['YMax'] * appendedDetections['imageHeight']

            # Writing to disk
            appendedDetections.to_csv(f"open-images-v6/{type}/labels/detections.csv")    






if __name__=='__main__':
    main()
