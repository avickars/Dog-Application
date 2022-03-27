# petfinder

This directory contains the scripts used to scrape the data from petfinder.com

## Requirements
- beautifulsoup4 4.10.0
- pandas 1.4.1
- selenium 4.1.2

## scraping_links.py

This script scrapes the urls to for 15 000 different dogs

## Scraping_data.py

This script scraps the images and attributes for 10 000 different dogs (using the generated links).

NOTE: scraping_links.py must be run first.