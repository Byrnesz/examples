from sklearn.datasets import fetch_20newsgroups
from sklearn import metrics
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
categories = ['alt.atheism', 'sci.space']
newsgroups_train = fetch_20newsgroups(subset='train',
                                      remove=('headers', 'footers', 'quotes'),
                                      categories=categories)
vectors = vectorizer.fit_transform(newsgroups_train.data)
clf = BernoulliNB(alpha=.01)
clf.fit(vectors, newsgroups_train.target)
newsgroups_test = fetch_20newsgroups(subset='test',
                                     remove=('headers', 'footers', 'quotes'),
                                     categories=categories)
vectors_test = vectorizer.transform(newsgroups_test.data)
pred = clf.predict(vectors_test)
metrics.f1_score(newsgroups_test.target, pred)

# 0.88555858310626712