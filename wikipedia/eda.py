import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation, naive_bayes

# dataset - https://github.com/zhangxiangxiao/Crepe/blob/master/README.md#components

header_rows = ['cl', 'title', 'content']
df = pd.read_csv('train.csv', names=header_rows)

df = df.query('cl == 1 or cl == 2')
df['clnew'] = df.cl.apply(lambda x: 1 if x == 1 else 0)

vectorizer = CountVectorizer(min_df=5, max_df=.3, ngram_range=(1,2))
X = vectorizer.fit_transform(df.content)
X = X.tocsc()
Y = df.clnew

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y)

clf = naive_bayes.MultinomialNB()
clf.fit(X_train, Y_train)
print "Accuracy: %0.2f%%" % (100 * clf.score(X_test, Y_test))