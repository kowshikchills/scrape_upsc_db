from tqdm import tqdm
import pickle
import boto3

__TableName__ = 'upsc_training_data'
client  = boto3.client('dynamodb',region_name = 'ap-south-1')
DB  = boto3.resource('dynamodb',region_name = 'ap-south-1')
table = DB.Table(__TableName__)

tags = []
c = 0
for i in tqdm(range(27000)):
    try:
        item = table.get_item(Key={'TrainId':i})
        tags = tags + item['Item']['tags']
    except:
        c = c+1

with open('data/tags.pkl', 'wb') as f:
    pickle.dump(tags, f)