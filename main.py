import tweepy
import requests
import os
import re
import time
import random

#List of words to replace
keywords = ['migrant','migrants','réfugié','refugie','réfugiés','refugies','réfugie','refugié','réfugies','refugiés']
emoji = ['']

# Consumer keys and access tokens, used for OAuth
consumer_key = 'WUuDXUQswVWWwRqjYYrikfu62'
consumer_secret = 'uFJuiHxopWCtTPkF65Uko7sv7krabx9K7KbqMmcytQ7A0TIvoh'
access_token = '837361062-Ua30HK9ajAnR07XOEG6v4f5aIG9dq9wIEzWwHKTa'
access_token_secret = 'x8bG3jDZx96JqGSDguFAquZLx2Nv6uTpTEhLQqkJfXJWV'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
# Sample method, used to update a status
# api.update_status('Hello Python Central! #twitterisart')


def find():
   listoftweet = []
   for tweet in tweepy.Cursor(api.search,
                             q="migrant OR migrants OR MIGRANT OR MIGRANTS OR refugies OR refugie 0R REFUGIES OR REFUGIE",
                             result_type="recent",
                             lang="fr").items(5):

      listoftweet.append(tweet.text)
      screen_name = tweet.author.screen_name.encode('utf8')

   print len(listoftweet)
   text = random.choice(listoftweet)
   newlist = []
   words = text.split()

   for word in words:
     if any(keyword in word.lower() for keyword in keywords):
       newlist.append(u'\U0001f466\U0001f3ff')
     else:
       newlist.append(word)
   #newlist = words[4:len(words)]

   if newlist[0] == 'RT':
     newlist.pop(0)
     newlist.pop(0)
   string = " ".join(newlist)
   #string = re.sub(r'[^\x00-\x7F]+','', string)
   string = re.sub('htt(\S+)\s?','' , string)
   string = re.sub(' +',' ',string)
   string = string[:-1] if string.endswith(' ') else string
   string_final = string+" @"+screen_name
   return(string_final)

def post(text):
 api.update_status(text)
 print 'POSTING'

 
 
while True:
    try:
        text = find()
        print text
        while True:
         if len(text) > 140:
             text = find()
         else:
             post(text)

    except tweepy.TweepError:
        time.sleep(60*2)
        continue
    except StopIteration:
        break 

  
