import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import os

base_url = 'https://github.com'


def scrape_all_topics():
    # topics_url = get_topics_url(base_url + '/topics')
    topics_url = read_topics_from_csv()

    # create a directory
    dir_name = 'topics_top_repos'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    for url in topics_url:
        scrape_each_topic(url)


def scrape_each_topic(topic_url):
    topic_doc = download_page(topic_url)

    file_name = 'topics_top_repos/' + topic_url.split('/')[-1] + '.csv'
    if os.path.exists(file_name):
        print('The file {} already exists. Skipping...'.format(file_name))
        return

    # Get title, username, url and star for each repo
    h3_selector = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class': h3_selector})

    repo_usernames = []
    repo_titles = []
    repo_urls = []
    for repo in repo_tags:
        a_tags = repo.find_all('a')
        repo_usernames.append(a_tags[0].text.strip())
        repo_titles.append(a_tags[1].text.strip())
        repo_urls.append(base_url + a_tags[1]['href'])

    # Get list of stars for each repo
    star_selector = 'Counter js-social-count'
    star_tags = topic_doc.find_all('span', {'class': star_selector})

    repo_stars = [parse_star_count(star_tag.text) for star_tag in star_tags]

    # repo dict
    repo_dict = {'repo_username': repo_usernames, 'repo_name': repo_titles, 'stars': repo_stars, 'repo_url': repo_urls}

    topic_repos_df = pd.DataFrame(repo_dict)

    print('Creating file {}...'.format(file_name))
    # Dump all info to csv
    topic_repos_df.to_csv(file_name, index=None)


def download_page(url):
    response = re.get(url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))

    # parse webpage using Beautiful Soup
    response_doc = BeautifulSoup(response.text, 'html.parser')
    return response_doc


def get_topics_url(url):
    res_doc = download_page(url)
    topics_url_selector = 'no-underline flex-1 d-flex flex-column'
    topics_url_tags = res_doc.find_all('a', {'class': topics_url_selector})
    topic_urls = [base_url + tag['href'] for tag in topics_url_tags]
    return topic_urls


def parse_star_count(star_str):
    star_str = star_str.strip()
    if star_str[-1] == 'k':
        return int(float(star_str[:-1]) * 1000)
    return int(star_str)


def read_topics_from_csv():
    df = pd.read_csv('topics.csv')
    topic_urls = df['topic_url'].tolist()
    return topic_urls


scrape_all_topics()
