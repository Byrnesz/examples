import numpy as np
import pandas as pd
from lxml import html
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation, naive_bayes

def clean(text):
	# score w/ LR - 0.95974
    return html.fromstring(text).text_content().lower().strip()


from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
def rev_to_words(raw_review):
	# score w/ LR - 0.95660
    review_text = BeautifulSoup(raw_review).get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    useful_words = [w for w in words if not w in stops]
    return(" ".join(useful_words))

tr_data = pd.read_csv('labeledTrainData.tsv', delimiter='\t')
te_data = pd.read_csv('testData.tsv', delimiter='\t')

trX = [clean(text) for text in tr_data['review'].values]
trY = tr_data['sentiment'].values

vect = TfidfVectorizer(min_df=10, ngram_range=(1, 2))
trX = vect.fit_transform(trX)

ids = te_data['id'].values
teX = [clean(text) for text in te_data['review'].values]
teX = vect.transform(teX)

model_log = LR()
model_log.fit(trX, trY)
pr_teX_log = model_log.predict_proba(teX)[:, 1]
pd.DataFrame(np.asarray([ids, pr_teX_log]).T).to_csv('log.csv',index=False,header=["id", "sentiment"])


# score - 0.89864
model_lin = LinearSVC()
model_lin.fit(trX, trY)
pr_teX_lin = model_lin.predict(teX)
pd.DataFrame(np.asarray([ids, pr_teX_lin]).T).to_csv('linsvc.csv', index=False, header=["id", "sentiment"])


# accuracy - 87.25%
pos = []
neg = []
for num, row in tr_data.iterrows():
    if row.sentiment == 1:
        pos.append({'rev': row.review, 'pos': True})
    else:
        neg.append({'rev': row.review, 'pos': False})
df = pd.DataFrame.from_records(pos + neg)
vectorizer = CountVectorizer(min_df=5, max_df=.3, ngram_range=(1,2))
X = vectorizer.fit_transform(df.rev)
X = X.tocsc()
Y = df.pos.values.astype(np.int)
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,Y)
clf = naive_bayes.MultinomialNB(fit_prior=False, alpha=0.5)
clf.fit(X_train, Y_train)
print "Accuracy: %0.2f%%" % (100 * clf.score(X_test, Y_test))