import tweepy
import requests
import os
import re
import time
import random

#List of words to replace
keywords = ['animal','dog','cat']

#list of emojis that you want to put
emojis = [u'\U0001F427',u'\U0001F424']


# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
# Put the keyword in a string to send it to Twitter
keyword = ''
for x in range(0,len(keywords)):
 if(x != len(keywords)-1):
  keyword = keyword+keywords[x]+" OR "+keywords[x].upper()+" OR "
 else:
  keyword = keyword+keywords[x]+" OR "+keywords[x].upper()
  
# Function to find a tweet with our keywords, change the lang to a specific language (fr,en,sp,...)
def find():
   listoftweet = []
   for tweet in tweepy.Cursor(api.search,
                             q=keyword,
                             result_type="recent",
                             lang="en").items(50):

      listoftweet.append(tweet.text)
      screen_name = tweet.author.screen_name.encode('utf8')

   # Here I put all the tweet found in a list and then choose one randomly
   text = random.choice(listoftweet)
   newlist = []
   words = text.split()
   
   # This part is about the finding of our keywords and to repalce them with an random emoji from our list
   for word in words:
     if any(keyword in word.lower() for keyword in keywords):
       newlist.append(random.choice(emojis))
     else:
       newlist.append(word)
  
  # here is some line about the purging our final tweet
   if newlist[0] == 'RT':
     newlist.pop(0)
     newlist.pop(0)
   string = " ".join(newlist)
   #string = re.sub(r'[^\x00-\x7F]+','', string)
   string = re.sub('htt(\S+)\s?','' , string)
   string = re.sub(' +',' ',string)
   string = string[:-1] if string.endswith(' ') else string
   string_final = string+" (via @"+screen_name+")"
   return(string_final)

# function to post the final tweet
def post(text):
 api.update_status(text)
 print 'POSTING'

 
# Security part ! To avoid the character and rate of query limitation
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
     # I put 15min to avoid the rate of query limitation
        time.sleep(60*15)
        continue
    except StopIteration:
        break 
