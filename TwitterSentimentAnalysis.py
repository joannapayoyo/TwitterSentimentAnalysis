import datetime
import sys
import jsonpickle
import os
import json
import tweepy
from tweepy import OAuthHandler

# Replace the API_KEY and API_SECRET with your application's key and secret.
ckey="XjFwLTGuvCYX3PUoPHDoCMbT1"
csecret="KeIa69uyKAAv6jeCLaT1lC19Y6Q7vI0upsIrVeAMwKZq4yHvmA"
atoken="228985267-ZiPdBxOnpjMxgGaD1y2pnE1W05UzqjB4RTjD1GCI"
asecret="WACvIuXKj3quOZf8bK3UjFjgrJzY4Q3lO6kyMhrMR3woQ"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
 
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
    
searchQuery = "stem"  # this is what we're searching for
filterText = 'women' #To filter returned tweets based on a second filter
maxTweets = 1000# Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = 0

tweetCount = 0
print("Max of {0} tweets are requested".format(maxTweets))


#To filter returned tweets based on a second filter
def tweetFilter(text, filterText):
    if((filterText in text) or ('science' in text)):
        return True
    else:
        return False


fName = "res.txt".format(tweetCount) # We'll store the tweets in a text file.
f= open(fName,encoding='utf-8', mode='w')

loopMax = 20
loopCounter = 0

while ((tweetCount < maxTweets) and (loopCounter < loopMax)):
    loopCounter += 1  
    try:
        if (not sinceId):
            new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang="en",max_id=str(max_id - 1))
        else:
            new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang="en",max_id=str(max_id - 1),since_id=sinceId)

        if not new_tweets:
            #print("No more tweets found")
            break
                
        for tweet in new_tweets:
            #tweetJson = jsonpickle.encode(tweet._json, unpicklable=False)
            #f.write(tweetJson +'\n')
            #f.write(tweet._json['text'] +'\n')
            if (tweetFilter(tweet._json['text'], filterText)):
                f.write(tweet._json['created_at'] +','+  tweet._json['text']  +'\n')
                #f.write(str(tweet._json) +'\n'+'<<<<<<<<<<<<<<<<<<***>>>>>>>>>>>>>>>'+'\n')
                tweetCount +=1
        #tweetCount += len(new_tweets)

        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print("Downloaded {0} tweets".format(tweetCount))
f.close()
#print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, "~/Desktop/fName.txt"))
