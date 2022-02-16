import pandas as pd

def main():
    # Removing Non Dog Boxes

    test = pd.read_csv('open-images-v6/test/labels/detections.csv')
    test = test[test['LabelName'] == '/m/0bt9lr']
    test.to_csv('open-images-v6/test/labels/detections.csv')

    train = pd.read_csv('open-images-v6/train/labels/detections.csv')
    train = train[train['LabelName'] == '/m/0bt9lr']
    train.to_csv('open-images-v6/train/labels/detections.csv')

    validation = pd.read_csv('open-images-v6/validation/labels/detections.csv')
    validation = validation[validation['LabelName'] == '/m/0bt9lr']
    validation.to_csv('open-images-v6/validation/labels/detections.csv')



if __name__=='__main__':
    main()
