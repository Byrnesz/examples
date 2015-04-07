from indicoio import text_tags
from email_reply_parser import EmailReplyParser
import json
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords


def text_tags_words_sliding(messages, window=100, shift=20):
    allwords = []
    data = {}
    for m in messages:
        # if this is not a sent message
        if "\\Sent" not in m.get('folders', tuple()):
            continue
        if not m.get('body') or not m['body'].get('content'):
            continue
        allwords.extend(extract_words(email_to_words(EmailReplyParser.parse_reply(m['body']['content']))))
    return allwords
    # current_window = 0
    # next_window = window
    # while True:
    #     # have we reached the end
    #     if len(allwords) < next_window:
    #         print "sliding-text-tags reached end at lengths:%s" % len(allwords)
    #         break
    #     print "sliding-text-tags start:%s end:%s" % (current_window, next_window)
    #     data[current_window] = ' '.join(allwords[current_window:next_window])
    #     data[current_window] = text_tags(data[current_window])
    #     current_window += shift
    #     next_window += shift
    # return data


def email_to_words(raw_review):
    review_text = BeautifulSoup(raw_review).get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    useful_words = [w for w in words if not w in stops]
    return useful_words
    # return " ".join(useful_words)

def extract_words(sentence):
    # replace all non-word characters with empty space
    return re.split(r" +", re.sub(r'[+{}=_\'"*,<>!?:;()\[\]\/\\.@]+', ' ', sentence).strip())

f = open('email_4_1.json','r')
rawemails = json.load(f)
# print len(rawemails)
f.close()

data = text_tags_words_sliding(rawemails)
print data
# f = open('e2w.txt','w')
# f.write(data) # python will convert \n to os.linesep
# f.close()