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
import boto3
from scrape_utils.utils import MongoDB_Train_Data, get_all_deets, create_item

__TableName__ = 'upsc_training_data'
client  = boto3.client('dynamodb',region_name = 'ap-south-1')
DB  = boto3.resource('dynamodb',region_name = 'ap-south-1')
table = DB.Table(__TableName__)
with open('data/article_links.pkl', 'rb') as handle:
    article_links = pickle.load(handle)

failed_articles = []
for i in tqdm(range(len(article_links))):
    try: 
        artcl_link, date, heading, art_text, art_types, key_points_isin, summary, tags = get_all_deets(article_links[i])
        item = create_item(i,artcl_link, date, heading, art_text, art_types, key_points_isin, summary, tags)
        response = table.put_item(Item  = item)
    except:
        failed_articles.append(article_links[i])

with open('data/failed_articles.pkl', 'wb') as f:
    pickle.dump(failed_articles, f)