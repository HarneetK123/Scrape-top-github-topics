# Scrape top github topics
This is a python crawler script to scrape top github topics and top repositories for each topic

## Pre-requisties:
1. Python - Install from [here](https://www.python.org/downloads/)
2. beautifulSoup - `pip install beautifulsoup4`
3. Pandas - `pip install pandas`

This repository contains 2 scripts:
1. extract_top_topics.py - This script extracts all the top topics from `https://github.com/topics` and generates a csv file `topics.csv`. The csv file has three columns topic title, topic description and topic url.
2. scrape_each_topic.py - This script gets the topic urls by reading `topics.csv` and crawls through each topic to collect data and stores in a csv file. Each file has username, repo name, stars and repo url columns.
