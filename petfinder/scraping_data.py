import requests
import pprint
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import shutil
import urllib.request


def images_links(imageObjects):
    img_counter = 1

    substring = '/'

    images = []

    for image in imageObjects:
        images.append(image['src'])

    unique_images = []

    for i in range(len(images)):
        substring = substring + str(img_counter) + "/"
        if (substring in images[i]):
            unique_images.append(images[i])
        substring = '/'
        img_counter = img_counter + 1

    return unique_images

def dog_attributes(soup):
    # Getting the dog name
    dog_name = soup.find(attrs={"data-test": "Pet_Name"})

    # Normalizing the dog name
    dog_name = re.sub('\s+', '', dog_name.contents[0]).lower()  # remove \n, tabs and spaces from string

    # Extracting dog breed
    dog_breed = soup.find(attrs={"data-test": "Pet_Breeds"}).text.strip().lower()

    # Extracting dog age
    dog_age = soup.find(attrs={"data-test": "Pet_Age"}).text.strip().lower()

    # Extracting dog sex
    dog_sex = soup.find(attrs={"data-test": "Pet_Sex"}).text.strip().lower()

    # Extracting dog size
    dog_size = soup.find(attrs={"data-test": "Pet_Full_Grown_Size"}).text.strip().lower()


    return {'name': dog_name, 'breed': dog_breed,'age':dog_age, 'sex':dog_sex, 'size':dog_size}



def main():
    # Making the directory to store the dogs
    # Checking if directory already exists
    if not os.path.exists('dogs'):
        os.mkdir('dogs')

    # Reading in the pet links
    links = pd.read_csv('pet_links.txt',names=['links'])

    # Defining list to hold attributes
    dogInfo = []

    # Defining counter to define the number of successful downloads
    numSuccessfulDownloads = 0

    # Pred
    try:
        info = pd.read_csv('attributes.csv')
        alreadyDownloadedLinks = info['link'].values
    except FileNotFoundError:
        info = pd.DataFrame()
        alreadyDownloadedLinks = []

    # Iterating through each link
    for index, link in links.iterrows():
        # Subsetting to get the link
        link = link['links']

        # If we have already downloaded this dogs info, skip it
        if link in alreadyDownloadedLinks:
            continue

        # Getting the html
        page = requests.get(link)

        # Parsing html
        soup = BeautifulSoup(page.content, "html.parser")

        # Getting the unique image links
        imageLinks = images_links(soup.find_all('img'))

        # If this dog has 1 or less images, we skip it
        if len(imageLinks) <= 1:
            continue

        # Getting the dog attributes
        attributes = dog_attributes(soup)

        # Making the directory for this dog
        os.mkdir(f"dogs/dog_{index}")

        # Appending to the attributes
        attributes['path'] = f"dog_{index}"
        attributes['numImages'] = len(imageLinks)

        # Downloading images
        imageCounter = 0
        for imageLink in imageLinks:
            dog_image_name = f"dogs/dog_{index}/img_{imageCounter}.jpg"
            urllib.request.urlretrieve(imageLink, dog_image_name)
            imageCounter += 1

        attributes['downloadedImages'] = imageCounter
        attributes['link'] = link

        dogInfo.append(attributes)

        numSuccessfulDownloads += 1

        if numSuccessfulDownloads % 100 == 0:
            print(f"{round((numSuccessfulDownloads / 10000) * 100, 3)} %")

            print(f"{round((index / 15000) * 100, 3)} %")

            # Saving attributes info in case download breaks
            info = info.append(dogInfo, ignore_index=True)
            info.to_csv('attributes.csv')


        if numSuccessfulDownloads >= 10000:
            break

    info = info.append(dogInfo, ignore_index=True)

    info.to_csv('attributes.csv')





if __name__=='__main__':
    main()