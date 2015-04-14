import json
import os
import time
from Queue import Queue
from threading import Thread
import datetime
from requests.exceptions import ChunkedEncodingError
import contextio
import logging
from cred import *


class OpbeatLogger():
    def __init__(self):
        formatter = logging.Formatter(
            '%(asctime)s:%(process)s:%(thread)d:%(name)s:%(levelname)s:%(filename)s:%(funcName)s():%(lineno)d:%(message)s')
        logger = logging.getLogger()
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    def captureException(self):
        logging.exception('OpebatException:')


# maximum number of retries before job is abandoned, display error
MAX_RETRIES = 5
# number of threads to download emails
NUM_THREADS = 3
SECONDS_TO_SLEEP = 5
WORKER_MAX_SECONDS_TO_SLEEP = 60
MESSAGES_LIMIT = 50
SLEEP_CONTEXTIO_EXCEPTION = 15
CONTEXTIO_MAX_RETRIES_DOWNLOAD_THREAD = 10
MAX_THREAD_RETRIES = 2
opbeat = OpbeatLogger()


def clean_message_body(m):
    del m['files']
    del m['parent']
    del m['base_uri']
    del m['date_indexed']  # when was it indexed in context.io
    if m.get('gmail_message_id'):
        del m['gmail_message_id']
        del m['gmail_thread_id']
    del m['list_headers']
    del m['email_message_id']
    del m['facebook_headers']
    del m['sources']
    del m['person_info']
    if m.get('thread'):
        del m['thread']
    # sometimes body is in both html + text forms, just need the text-form
    if m['body']:
        if len(m['body']) == 2:
            for index, body in enumerate(m['body']):
                if body['type'] == 'text/html':
                    m['body'].remove(body)
        m['body'] = m['body'][0]


def get_messages(account, queue_nr):
    retries = 0
    while True:
        try:
            return account.get_messages(
                include_body=1,
                offset=queue_nr * MESSAGES_LIMIT,
                body_type='text/plain',
                limit=MESSAGES_LIMIT)
        except (ValueError, ChunkedEncodingError, Exception) as e:
            # contextio issue, pause and try again
            retries += 1
            print 'Contextio error %s,wait %s seconds retries:%s' % (str(e), SLEEP_CONTEXTIO_EXCEPTION, retries)
            time.sleep(SLEEP_CONTEXTIO_EXCEPTION)
            # dont log the exception if it says:
            # account is not valid, since account was validated earlier
            # invalid json object returned
            if not ('account' in str(e) and 'is invalid' in str(e)) and \
                    not 'No JSON object could be decoded' in str(e) and \
                            'Expecting value: line 1 column 1 (char 0)' not in str(e) and \
                            "HTTPSConnectionPool(host='api.context.io', port=443)" not in str(e) and \
                            e.__class__ != ChunkedEncodingError:
                opbeat.captureException()
            if retries > 5:
                print "skipping queue:%s after %s retries" % (queue_nr, retries)
                return tuple()


def download_batch(q, allmessages, account):
    while True:
        queue_nr = q.get()
        dict_messages = []
        for message in get_messages(account, queue_nr):
            message_dict = message.__dict__
            clean_message_body(message_dict)
            dict_messages.append(message_dict)
        allmessages.extend(dict_messages)

        print 'queue:%s offset:%s, allmessages:%s' % (queue_nr, queue_nr * MESSAGES_LIMIT, len(allmessages))
        if dict_messages:
            q.put(queue_nr + NUM_THREADS)
        q.task_done()


def download(account_id):
    start_time = datetime.datetime.utcnow()

    account = contextio.Account(context_io, {'id': account_id})
    # validate that the account exist on context.io
    try:
        account.get()
    except Exception as e:
        if "invalid signature" in str(e).lower():
            print "Bad contextio credentials. %s" % e
        else:
            print "Contextio error %s. the account isn't registered w/ context.io or the 'email_id' is invalid." % e
            opbeat.captureException()
        return
    print 'found contextio account - Starting Download'

    # download emails
    allmessages = []

    q = Queue(maxsize=0)
    for i in range(NUM_THREADS):
        worker = Thread(target=download_batch, args=(q, allmessages, account))
        worker.setDaemon(True)
        worker.start()

    for x in range(NUM_THREADS):
        q.put(x)
    q.join()

    if not allmessages and account.nb_messages:
        print "Can't download emails, context.io is probably syncing"
        return

    # if there aren't emails
    if not allmessages and not account.nb_messages:
        print "There aren't any messages in the account on contextio, syncing issue, try again later."
        return
    if allmessages:
        # sort messages by timestamp
        allmessages = sorted(allmessages, key=lambda k: k['date'])
        file_path = "../email.json"
        with open(file_path, 'wb') as f:
            f.write(json.dumps(allmessages))
        download_time = (datetime.datetime.utcnow() - start_time).total_seconds()
        print "Downloaded emails to %s. Download time %s seconds" % (file_path, download_time)
    return

# configure context.io credential strings after setting up acct
if __name__ == '__main__':
    context_io = contextio.ContextIO(
        consumer_key = c_key,
        consumer_secret = c_secret
    )

    email_id = eid
    download(email_id)
