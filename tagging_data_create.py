import pickle
import pandas as pd
with open('data/tags.pkl', 'rb') as handle:
    tags = pickle.load(handle)
with open('data/headings.pkl', 'rb') as handle:
    headings = pickle.load(handle)
df = pd.DataFrame()
df['headings'] = headings
df['tags'] = tags
df['TrainId'] = np.arange(len(df))
df.to_pickle('UIdata/data_tagging.pkl')