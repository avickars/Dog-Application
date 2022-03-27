# open-images-processing

This directory contains the code used to download and clean the open images data set.

## Requirements
- pandas 1.4.1
- fiftyone 0.14.4
- PIL 8.4.0

## download_open_images.py

### Description

This script downloads the open images data set to the current working directory.

### To run

python download_open_images.py

###

## process_open_images.py

### Description

This script cleans the open images' dataset contained in the "open-images-v6" directory in the current working directory.

### To run

python process_open_images_.py

Note: You must run download_open_images.py first, and have "open-images-v6" in youy current working directory.