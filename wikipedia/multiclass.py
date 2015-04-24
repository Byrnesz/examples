import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation, naive_bayes

header_rows = ['cl', 'title', 'content']
df = pd.read_csv('train.csv', names=header_rows)

vectorizer = CountVectorizer(min_df=5, max_df=.3, ngram_range=(1,2))
X = vectorizer.fit_transform(df.content)
X = X.tocsc()
Y = df.cl

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y)

clf = naive_bayes.MultinomialNB()
clf.fit(X_train, Y_train)
print "Accuracy: %0.2f%%" % (100 * clf.score(X_test, Y_test))