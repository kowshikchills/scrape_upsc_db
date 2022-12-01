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
from collections import Counter

from sentence_transformers import SentenceTransformer
import pandas as pd 
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df =pd.read_csv('label_keys.csv')
tags_order = [i[0] for i in Counter([i.lower() for i in df['label'].dropna()]).most_common()][::-1]
del df['count']
tag_map = df.set_index('keys_').to_dict('index')
total_tags = list(tag_map.keys())

df_data = pd.read_pickle('UIdata/data_tagging.pkl')
tags_sent = df_data['tags'].values[120]
def get_labels(tags_sent):
    labels = []
    for i in tags_sent:
        tag = i.lower()
        if tag in total_tags:
            labels.append(tag_map[tag]['label'])
    if len(labels)> 0:
        return([tags_order[j] for j in [tags_order.index(i) for i in labels]][0])
    else:
        return('None')
labels_class = []
for i in tqdm(df_data['tags'].values):
    labels_class.append(get_labels(i))

df_data['label'] = labels_class


labels = ['Environment','History','Culture','Geography','International Relations',
'Polity','Governance','Health','Society','Economy','Science&Technology','Defence','Agriculture','sports']
labels = [i.lower() for i in labels]
model = SentenceTransformer('bert-base-nli-mean-tokens')
embeddings_tags = model.encode(labels)
most_relevant = []
next_relevant = []
for i in tqdm(range(len(df_data))):
    key__ = df_data.headings.values[i]
    embeddings_key = model.encode(key__)
    probs = cosine_similarity([embeddings_key],embeddings_tags)
    label_index = np.argmax(probs)
    most_relevant.append(labels[label_index])

df_data['label_transformer'] = most_relevant
df_data.to_pickle('data/data_labels_final.pkl')