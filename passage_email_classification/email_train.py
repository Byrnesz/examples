# TODO: use scikit-learn datasets
# compare with small & large datasets
# regex garbage, puctuation, and remove NaNs from emails
# compare w/ max entropy + tfidf
# predict proba

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
from passage.preprocessing import Tokenizer
from passage.layers import Embedding, GatedRecurrent, Dense
from passage.models import RNN
from passage.utils import save, load

gid = pd.read_json('email.json')
mom = pd.read_json('mom.json')

g_emails = []
m_emails = []
for email in gid.body:
    if email != []:
        g_emails.append({'gids': True, 'body': email['content'].encode(errors='ignore')})
for email in mom.body:
    if email != []:
        m_emails.append({'gids': False, 'body': email['content'].encode(errors='ignore')})
df = pd.DataFrame.from_records(g_emails + m_emails)

vectorizer = CountVectorizer(min_df=5, max_df=.3, ngram_range=(1,2))
X = vectorizer.fit_transform(df.body)
X = X.tocsc()
Y = df.gids.values.astype(np.int)

ntest = int(len(df) * .7) # TODO: use train_test_split from scikit
X = [word for word in df.body.values if word]
Y = df.gids.values
X_train = X[:-ntest]
X_test  = X[-ntest:]
Y_train = Y[:-ntest]
Y_test  = Y[-ntest:]

print X_train[3:4][0] # example email 

tokenizer = Tokenizer(min_df=10, max_features=50000)
X_train = tokenizer.fit_transform(X_train)
X_test = tokenizer.transform(X_test)
print tokenizer.inverse_transform(trX[1:2]) #see what words are kept
print tokenizer.n_features

layers = [
    Embedding(size=128, n_features=tokenizer.n_features),
    GatedRecurrent(size=128, ),
    Dense(size=1, activation='sigmoid', init='orthogonal')
]

model = RNN(layers=layers, cost='BinaryCrossEntropy')
for i in range(2):
    model.fit(X_train, Y_train, n_epochs=1)
    tr_preds = model.predict(X_train[:len(Y_test)])
    te_preds = model.predict(X_test)
    
    tr_acc = metrics.accuracy_score(Y_train[:len(Y_test)], tr_preds > 0.5)
    te_acc = metrics.accuracy_score(Y_test, te_preds > 0.5)
    
    print i, tr_acc, te_acc

# Epoch 0 Seen 2015 samples Avg cost 0.2800 Time elapsed 55 seconds
# 0 0.960209881941 0.0
# Epoch 0 Seen 2015 samples Avg cost 0.1200 Time elapsed 54 seconds
# 1 0.969392216878 0.147488755622

save(model, 'save_test_2_22.pkl')
pd.read_pickle('save_test_2_22.pkl')