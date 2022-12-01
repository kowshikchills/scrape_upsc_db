from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import nltk
from nltk import sent_tokenize
nltk.download('punkt')
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from setfit import SetFitModel, SetFitTrainer
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
import datasets
from datasets import Dataset, DatasetDict
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_pickle('data/training_data.pkl')
df = df[['headings','label']]
map_ = {}
c = 0
for i in np.unique(df['label'].values):
    map_[i] = c
    c = c+1
df['label_text'] = df['label']
df['label'] =  df['label'].replace(map_)
df.columns = ['text','label','label_text']
df = df.sample(len(df[:10]))

df['type_'] = ['train']*int(0.75*len(df)) + ['test']*(len(df) - int(0.75*len(df)))
df_train = df[df['type_'] == 'train']
del df_train['type_']
df_test = df[df['type_'] == 'test']
del df_test['type_']
train_ds = Dataset.from_pandas(df_train)
test_ds = Dataset.from_pandas(df_test)

model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")
trainer = SetFitTrainer(
    model=model,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    loss_class=CosineSimilarityLoss,
    batch_size=16,
    num_iterations=20,
    num_epochs=1
)
trainer.train()
metrics = trainer.evaluate()
model.push_to_hub('upsc-classification-model-v1',token='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')