"""Divide up text block into tweets"""

import requests
from requests_oauthlib import OAuth1
import time

TEXT=open("federalist.txt","r")

CHUNKED_TEXT = TEXT.read().split("\n\n")

def create_chunks():
    for chunk in CHUNKED_TEXT:
        chunk = chunk.replace("\n", " ")
        remainder = len(chunk)
        while remainder > 0:
            if len(chunk) > 140:
                knuhc = chunk[:139]
                knuhc = knuhc[::-1]
                knuhc = knuhc.split(" ",1)
                tweet_length = len(knuhc[0])
                tweet = chunk[:139-tweet_length]
                chunk = chunk[139-tweet_length:]
                remainder = len(chunk)
                yield(tweet)
            else:
                remainder = 0
                yield(chunk)

# for tweet in create_chunks():
#     print(tweet)

def tweet(text):
    base_url = "https://api.twitter.com/1.1/statuses/update.json"
    payload = {
        "status": text,
        "display_coordinates": "false",
        }
    auth = OAuth1('MOFzgeRyg9KHhIRNpX90Sqefu', 'tdqULHQK0bXSF7zeCJMm0ICUmGMgc8VoKzWmDxvgTa5A5Ay3JY',
        '882755550047608832-QBJTXZVkSzB6InirdAED5GATZ0UCSK2', 'M4dUNodScnd7p9e8kMR93VZfG2mgWtw2a7ecUiMn590zN')
    result = requests.post(base_url, auth=auth, params=payload)
    print(result.json())

for update in create_chunks():
    tweet(update)
    time.sleep(60)
    