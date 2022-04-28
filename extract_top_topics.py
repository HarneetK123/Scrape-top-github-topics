import requests as re
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://github.com'


def scrape_topics():
    topics_url = 'https://github.com/topics'

    doc = download_page(topics_url)

    # find the `p` tags to get the popular topics, description and urls
    topics_title_class_selector = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topics_desc_class_selector = 'f5 color-fg-muted mb-0 mt-1'
    topics_url_selector = 'no-underline flex-1 d-flex flex-column'

    topics_title_tags = doc.find_all('p', {'class': topics_title_class_selector})
    topics_desc_tags = doc.find_all('p', {'class': topics_desc_class_selector})
    topics_url_tags = doc.find_all('a', {'class': topics_url_selector})

    # Generate list of titles, desc and url
    topic_titles = [tag.text for tag in topics_title_tags]
    topic_descriptions = [tag.text.strip() for tag in topics_desc_tags]
    topic_urls = [base_url + tag['href'] for tag in topics_url_tags]

    dataset_dict = {'topic_titles': topic_titles, 'topic_description': topic_descriptions, 'topic_url': topic_urls}

    # Create a dataframe from a dict
    topics_df = pd.DataFrame(dataset_dict)

    # dump data into csv
    topics_df.to_csv('topics.csv', index=None)


def download_page(url):
    response = re.get(url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))

    # parse webpage using Beautiful Soup
    response_doc = BeautifulSoup(response.text, 'html.parser')
    return response_doc
