import pickle
import pandas as pd
import itertools
from collections import Counter
with open('data/tags.pkl', 'rb') as handle:
    tags_list = pickle.load(handle)
''' 
tags = []
for i in tags_list:
    tags = tags + i
'''
tags = list(itertools.chain.from_iterable(tags_list))
months_str = ['january', 'february', 'march',
        'april', 'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december','current affairs','ibps']
tags = [i.lower() for i in tags]
for i in tags:
    for j in months_str:
        if j in i:
            try: 
                tags.remove(i)
            except:
                a = 1
dict_ = Counter(tags)
df = pd.DataFrame()
df['keys_'] = dict_.keys()
df['count'] = [dict_[i] for i in dict_.keys()]
df.to_csv('data/keys_upsc.csv')