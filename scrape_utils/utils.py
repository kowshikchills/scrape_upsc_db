from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import nltk
from nltk import sent_tokenize
nltk.download('punkt')
import warnings
import ast
warnings.filterwarnings(action='ignore')
import json 
from requests import get
import datetime
from datetime import date
from tqdm import tqdm
import pickle

class MongoDB_Train_Data:
    def __init__(self):

        pass
    def get_response_soup(self,url):
        response = get(url,verify=False, timeout=30)
        cleaned_response = response.text.replace('\x00', '')
        soup = BeautifulSoup(cleaned_response)
        return soup

    def get_all_articles_links(self, search_url):
        rec_soup = self.get_response_soup(search_url)
        pages = int(rec_soup.find(name = 'a',attrs = {'class':'last'}).text)
        articles = []
        for page in range(pages):
            pgurl = search_url + 'page/'+str(page+1)+'/'
            pgurl_soup = self.get_response_soup(pgurl)
            list_soup = pgurl_soup.find('div', attrs = {'class':'posts-listing'})
            article_list = list_soup.find_all(name = 'h1',attrs = {'id':'list'})
            for soup in article_list:
                articles.append(soup.find('a',href=True)['href'])
        return articles
    def get_entire_article_links_monthly(self):
        self.months_str = ['january', 'february', 'march',
         'april', 'may', 'june', 'july', 'august',
          'september', 'october', 'november', 'december']
        start = datetime.date(2013, 1, 1)
        end = date.today()
        date_generated = pd.date_range(start, end)
        to_scrape = np.unique(['-'.join(str(i).split('-')[:2]) for i in date_generated])
        self.entire_articles = []
        self.missing_months = []
        for i in tqdm(to_scrape):
            year = i.split('-')[0]
            month = self.months_str[int(i.split('-')[1]) -1]
            gk_search_url = 'https://www.gktoday.in/current-affairs/month/current-affairs-'+ month+'-'+year+'/'
            try:
                articles = self.get_all_articles_links(gk_search_url)
                self.entire_articles= self.entire_articles+articles
            except:
                self.missing_months.append(gk_search_url)
        with open('data/article_links.pkl', 'wb') as f:
            pickle.dump(self.entire_articles, f)

def get_response_soup(url):
    response = get(url,verify=False, timeout=30)
    cleaned_response = response.text.replace('\x00', '')
    soup = BeautifulSoup(cleaned_response)
    return soup
def get_all_deets(artcl_link):
    artcl_soup = get_response_soup(artcl_link)
    main_soup = artcl_soup.find('div', attrs = {'class':'inside_post column content_width'})
    heading = main_soup.find('h1').text
    date = main_soup.find('div', attrs = {'class': 'postmeta-primary'}).text
    art_text = []
    art_types = []
    summ_bool = False
    key_points_isin = 0
    summary = ''
    for x in main_soup:
        if (x.name in ['p','h4','l1','h3','l2','ul']) and (x.attrs == {}):
            if summ_bool:
                summary = x.text
                summ_bool = False
            else:
                art_text.append(x.text)
                art_types.append(x.name)
            if x.text == 'Key Points' or  x.text == 'Highlights':
                key_points_isin = 1
                summ_bool = True 
    tags = []
    try:
        topics = main_soup.find('b', text = re.compile('Topics:')).next_siblings
        for a in topics:
            if len(a.text.strip())>1:
                tags.append(a.text.strip())
    except:
        pass
    return artcl_link, date, heading, art_text, art_types, key_points_isin, summary, tags

def create_item(i,artcl_link, date, heading, art_text, art_types, key_points_isin, summary, tags):
    item = {
        'TrainId': i,
        'link': artcl_link,
        'date':date,
        'heading': heading,
        'article_text': art_text,
        'article_types': art_types,
        'summary_bool': key_points_isin,
        'summary':summary,
        'tags':tags
        
    }
    return(item)