import datetime
import pandas as pd
from requests import get
import datetime
from datetime import date
start = datetime.datetime.strptime("02-01-2020", "%d-%m-%Y")
end = datetime.datetime.strptime("07-08-2022", "%d-%m-%Y")
date_generated = pd.date_range(start, end)
tags = []
for i in tqdm(range(len(date_generated))):
    
    date = str(date_generated[i]).split(' ')[0]
    link = 'https://www.iasparliament.com/current-affairs/archives/'+date.replace('-','/')
    soup = get_response_soup(link)

    for i in soup.find_all(name = 'a',attrs = {'class':'label label-default label-default-cntrl tags'}):
        tags.append(i.text) 


from collections import Counter
tags_ = [i for i in tags if '-' in i]
dict_ = dict(Counter(tags_))
df_tags = pd.DataFrame()
df_tags['tags'] = tags_
df_tags['count'] = [dict_[i] for i in tags_]

df_tags.to_csv('valid_tags.csv')
