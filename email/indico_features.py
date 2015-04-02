from functions import get_bin_month, extract_words
from indicoio import sentiment, political, text_tags
from email_reply_parser import EmailReplyParser


from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
def email_to_words(raw_review):
    review_text = BeautifulSoup(raw_review).get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    useful_words = [w for w in words if not w in stops]
    return useful_words


def sentiment_words_sliding(messages, window=1000, shift=20):
    allwords = []
    data = {}
    for m in messages:
        if "\\Sent" not in m.get('folders', tuple()):
            continue
        if not m.get('body') or not m['body'].get('content'):
            continue
        allwords.extend(email_to_words(EmailReplyParser.parse_reply(m['body']['content'])))
    current_window = 0
    next_window = window
    print len(allwords)
    while True:
        if len(allwords) < next_window:
            print "sliding-sentiment reached end at lengths:%s" % len(allwords)
            break
        print "sliding-sentiment start:%s end:%s" % (current_window, next_window)
        data[current_window] = ' '.join(allwords[current_window:next_window])
        data[current_window] = sentiment(data[current_window])
        current_window += shift
        next_window += shift
    return data


import json
f = open('email_4_1.json','r')
rawemails = json.load(f)
print len(rawemails)
f.close()
data = sentiment_words_sliding(rawemails)
print data