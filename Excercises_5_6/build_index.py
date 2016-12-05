import requests
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')
print(r.content)

data = pd.DataFrame.from_csv('gazeta_articles.csv')
row_with_nan = np.where(pd.isnull(data))[0]
data = data.drop(data.index[row_with_nan])
data = data.reset_index(drop=True)
print(data.index)


for i in range(len(data)):
    tag = data.iloc[i]['tag']
    title = data.iloc[i]['title']
    text = data.iloc[i]['text']
    url = data.iloc[i]['url']
    print(i)
    es.index(index='gazetaru',
             doc_type=tag,
             id=i,
             request_timeout=50,
             body={
                 'title': title,
                 'text': text,
                 'url': url,
            })