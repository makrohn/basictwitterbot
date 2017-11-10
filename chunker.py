"""Divide up text block into tweets"""

import requests
from requests_oauthlib import OAuth1
import time

TEXT=open("federalist.txt","r")

CHUNKED_TEXT = TEXT.read().split("\n\n")

HANDLE = "@TweetFedPapers"

def create_chunks():
    for chunk in CHUNKED_TEXT:
        chunk = chunk.replace("\n", " ")
        remainder = len(chunk)
        while remainder > 0:
            if len(chunk) > 120:
                knuhc = chunk[:119]
                knuhc = knuhc[::-1]
                knuhc = knuhc.split(" ",1)
                tweet_length = len(knuhc[0])
                tweet = chunk[:119-tweet_length] + " " + HANDLE
                chunk = chunk[119-tweet_length:]
                remainder = len(chunk)
                yield(tweet)
            else:
                remainder = 0
                yield(chunk)

# for tweet in create_chunks():
#     print(tweet)

def tweet(text, replyto):
    base_url = "https://api.twitter.com/1.1/statuses/update.json"
    payload = {
        "status": text,
        "display_coordinates": "false",
        "in_reply_to_status_id": replyto
        }
    auth = OAuth1('MOFzgeRyg9KHhIRNpX90Sqefu', 'tdqULHQK0bXSF7zeCJMm0ICUmGMgc8VoKzWmDxvgTa5A5Ay3JY',
        '882755550047608832-QBJTXZVkSzB6InirdAED5GATZ0UCSK2', 'M4dUNodScnd7p9e8kMR93VZfG2mgWtw2a7ecUiMn590zN')
    result = requests.post(base_url, auth=auth, params=payload)
    return result.json()

inreply = ""

for update in create_chunks():
    answer = tweet(update, inreply)
    inreply = answer["id"]
    time.sleep(60)
    