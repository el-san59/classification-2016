from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import pandas as pd
import numpy as np



data = pd.DataFrame.from_csv('gazeta_articles.csv')
row_with_nan = np.where(pd.isnull(data))[0]
data = data.drop(data.index[row_with_nan])
data = data.reset_index(drop=True)

texts = data['tokens'].values

tfidf = TfidfVectorizer()
mat = tfidf.fit_transform(texts)
joblib.dump(tfidf, 'tfidf.model')
target = data['tag'].values

x_train, x_test, y_train, y_test = train_test_split(mat, target, test_size=.2)
model = SVC(kernel='linear')
model.fit(x_train, y_train)
joblib.dump(model, 'svc.model')
score = model.score(x_test, y_test)
print(score)

