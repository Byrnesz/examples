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
    # return(" ".join(useful_words))


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
        # have we reached the end
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


# def sentiment_words(messages):
#     windowsize = 10000
#     wordNum = 0
#     data_id = 0
#     data = {data_id: ''}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue

#         if wordNum > windowsize:
#             wordNum = 0
#             data_id += windowsize
#             data[data_id] = ""
#         content = email_to_words(EmailReplyParser.parse_reply(m['body']['content']))
#         data[data_id] += content + '\n'
#         wordNum += len(extract_words(content))

#     for bin, value in data.items():
#         data[bin] = sentiment(value)
#     return data


# def sentiment_month(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         month = get_bin_month(m['date'])
#         if not data.get(month):
#             data[month] = ""
#         data[month] += email_to_words(EmailReplyParser.parse_reply(m['body']['content'])) + '\n'

#     for k, v in data.items():
#         data[k] = sentiment(v)

#     return data


# def sentiment_email(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         # todo bulk!
#         data[m['date']] = sentiment(email_to_words(EmailReplyParser.parse_reply(m['body']['content'])))
#     return data


# def text_tags_words(messages):
#     windowsize = 10000
#     wordNum = 0
#     data_id = 0
#     data = {data_id: ''}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue

#         if wordNum > windowsize:
#             wordNum = 0
#             data_id += windowsize
#             data[data_id] = ""
#         content = email_to_words(EmailReplyParser.parse_reply(m['body']['content']))
#         data[data_id] += content + '\n'
#         wordNum += len(extract_words(content))

#     for key, value in data.items():
#         data[key] = text_tags(value)
#     return data


# def text_tags_month(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         month = get_bin_month(m['date'])
#         if not data.get(month):
#             data[month] = ""
#         data[month] += email_to_words(EmailReplyParser.parse_reply(m['body']['content'])) + '\n'

#     for k, v in data.items():
#         data[k] = text_tags(v)

#     return data


# def text_tags_words_sliding(messages, window=10000, shift=1000):
#     allwords = []
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         allwords.extend(extract_words(email_to_words(EmailReplyParser.parse_reply(m['body']['content']))))
#     current_window = 0
#     next_window = window
#     while True:
#         # have we reached the end
#         if len(allwords) < next_window:
#             print "sliding-text-tags reached end at lengths:%s" % len(allwords)
#             break
#         print "sliding-text-tags start:%s end:%s" % (current_window, next_window)
#         data[current_window] = ' '.join(allwords[current_window:next_window])
#         data[current_window] = text_tags(data[current_window])
#         current_window += shift
#         next_window += shift
#     return data


# def text_tags_email(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         # todo bulk
#         data[m['date']] = text_tags(email_to_words(EmailReplyParser.parse_reply(m['body']['content'])))
#     return data


# def political_sentiment_words(messages):
#     windowsize = 10000
#     wordNum = 0
#     data_id = 0
#     data = {data_id: ''}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue

#         if wordNum > windowsize:
#             wordNum = 0
#             data_id += windowsize
#             data[data_id] = ""
#         content = email_to_words(EmailReplyParser.parse_reply(m['body']['content']))
#         data[data_id] += content + '\n'
#         wordNum += len(extract_words(content))

#     for bin, value in data.items():
#         data[bin] = political(value)
#     return data


# def political_sentiment_month(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         month = get_bin_month(m['date'])
#         if not data.get(month):
#             data[month] = ""
#         data[month] += email_to_words(EmailReplyParser.parse_reply(m['body']['content'])) + '\n'

#     for k, v in data.items():
#         data[k] = political(v)

#     return data


# def political_sentiment_words_sliding(messages, window=10000, shift=1000):
#     allwords = []
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         allwords.extend(extract_words(email_to_words(EmailReplyParser.parse_reply(m['body']['content']))))
#     current_window = 0
#     next_window = window
#     while True:
#         # have we reached the end
#         if len(allwords) < next_window:
#             print "sliding-political-sentiment reached end at lengths:%s" % len(allwords)
#             break
#         print "sliding-political-sentiment start:%s end:%s" % (current_window, next_window)
#         data[current_window] = ' '.join(allwords[current_window:next_window])
#         data[current_window] = political(data[current_window])
#         current_window += shift
#         next_window += shift
#     return data


# def political_sentiment_email(messages):
#     data = {}
#     for m in messages:
#         if "\\Sent" not in m.get('folders', tuple()):
#             continue
#         if not m.get('body') or not m['body'].get('content'):
#             continue
#         print "doing:%s" % m['date'] # todo remove print
#         # todo bulk
#         data[m['date']] = political(email_to_words(EmailReplyParser.parse_reply(m['body']['content'])))
#     return data
