from indicoio import sentiment
from email_reply_parser import EmailReplyParser
import json
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords


def email_to_words(text):
    cl_text = BeautifulSoup(text).get_text()
    re_text = re.sub("[^\w]", " ", cl_text)
    words = re_text.lower().split()
    stops = set(stopwords.words("english"))
    useful_words = [w for w in words if not w in stops]
    return useful_words


def sentiment_sliding(messages, window=100, shift=20):
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


f = open('email.json','r')
rawemails = json.load(f)
print len(rawemails)
f.close()
data = sentiment_sliding(rawemails)
print data