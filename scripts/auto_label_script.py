from sentence_transformers import SentenceTransformer

import pandas as pd 
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
df = pd.read_csv('keys_upsc.csv')
df = df[df['count']>10]
del df['Unnamed: 0']

labels = ['Environment','History','Culture','Geography','International Relations',
'Polity','Governance','Health','Society','Economy','Science&Technology','Defence','Agriculture','sports']
labels = [i.lower() for i in labels]

model = SentenceTransformer('bert-base-nli-mean-tokens')
embeddings_tags = model.encode(labels)
most_relevant = []
next_relevant = []
for i in tqdm(range(len(df))):
    key__ = df.keys_.values[i]
    if '-' in key__:
        key__ = key__.replace('-',' ')
    embeddings_key = model.encode(key__)
    probs = cosine_similarity([embeddings_key],embeddings_tags)
    label_index = np.argmax(probs)
    most_relevant.append(labels[label_index])
df['label'] = most_relevant
