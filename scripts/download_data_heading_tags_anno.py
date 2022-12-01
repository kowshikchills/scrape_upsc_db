from tqdm import tqdm
import pickle
import boto3
import pandas as pd
import numpy as np

__TableName__ = 'upsc_training_data'
client  = boto3.client('dynamodb',region_name = 'ap-south-1')
DB  = boto3.resource('dynamodb',region_name = 'ap-south-1')
table = DB.Table(__TableName__)
tags = []
headings = []
c = 0
for i in tqdm(range(27000)):
    try:
        item = table.get_item(Key={'TrainId':i})
        tags.append(item['Item']['tags'])
        headings.append(item['Item']['heading'])
    except:
        c = c+1

with open('data/tags.pkl', 'wb') as f:
    pickle.dump(tags, f)
with open('data/headings.pkl', 'wb') as f:
    pickle.dump(headings, f)
    
df = pd.DataFrame()
df['headings'] = headings
df['tags'] = tags
df['TrainId'] = np.arange(len(df))
df.to_pickle('UIdata/data_tagging.pkl')