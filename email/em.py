import indicoio
indicoio.config.api_key = "YOUR_API_KEY"

from email_reply_parser import EmailReplyParser
import pickle
import json

def sentiment_sliding(messages, window=1000, shift=20):
    allwords = []
    data = {}
    for m in messages:
        if "\\Sent" not in m.get('folders', tuple()):
            continue
        if not m.get('body') or not m['body'].get('content'):
            continue
        allwords.append(EmailReplyParser.parse_reply(m['body']['content']))

    allwords = " ".join(allwords)
    allwords = allwords.encode('ascii','ignore')
    allwords = allwords.split()

    current_window = 0
    next_window = window
    print 'number of words', len(allwords)
    while True:
        if len(allwords) < next_window:
            print "sliding-sentiment reached end at lengths:%s" % len(allwords)
            break
        print "sliding-sentiment start:%s end:%s" % (current_window, next_window)
        data[current_window] = ' '.join(allwords[current_window:next_window])
        data[current_window] = indicoio.sentiment(data[current_window])
        print data[current_window]
        current_window += shift
        next_window += shift
    return data


f = open('email.json','r')
rawemails = json.load(f)
print 'number of emails', len(rawemails)
f.close()
data = sentiment_sliding(rawemails)
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

    
