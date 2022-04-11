# Dog-Application/webscraping

   This directory contains files related to webscraping


## get_multiple_dog_links_from_dynamic_webpage.ipynb

   This python notebook uses selenium to scrape the dogs' pages links
   from the dynamic search pages of petfinder.com

   The scraped links are downloaded and stored in pet_links.txt
   These links are stored locally so that we need not need to scrape the site
   again and again to get the dogs pages links.

## web-scraping-petfinder-multiple-pages-final.ipynb

   This python notebook goes through the links stored in pet_links.txt and
   scrapes the required dogs data available on those pages' links.

   It reuses most of the code of web-scraping-petfinder-single-page-final.ipynb

## web-scraping-petfinder-single-page-final.ipynb   

   This python notebook scrapes a single petfinder page that has dog's information
   and downloads the dog's images and dog's characteristics.

   Images are stored in a unique sub directory in the images folder.

   A unique subdirectory has this naming convention:
      dogname-breed-location
   For example:
      laila-pit-bull-terrier-mix-princegeorge-bc/

   If the unique subdirectory already exists then an integer number would be added as a suffix.
   For example:
      laila-pit-bull-terrier-mix-princegeorge-bc-1/

   Following dog metadata / characteristics are scraped and stored in a dog_name.csv inside that unique subdirectory:
      dog_name:  laila
      dog_breed:  Pit Bull Terrier Mix
      dog_city:  Prince George
      dog_state:   BC
      unique_dog_dir:  laila-pit-bull-terrier-mix-princegeorge-bc
      dog_age:  Young
      dog_sex:  Female
      dog_size:  Medium
      len(unique_images): 2

## pet_links.txt

   This file contains the petfinder pages' links that have dogs information.

## images/  

   This directory contains unique subdirectories with the dogs images
   and metadata scraped from petfinder.com

## web-scraping-petfinder-multiple-pages-final-test-and-error.ipynb

   This is a test file to test and record the errors encountered
   during the creation of get_multiple_dog_links_from_dynamic_webpage.ipynb.
