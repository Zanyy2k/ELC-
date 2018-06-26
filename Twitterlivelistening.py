import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler
import json
consumer_key = 'BaB4WM1AxMqxYws1zV4abyNZU'
consumer_secret = 'sVEIgNUhJePpfzzoUHpw4BfN81tm3DuUaMNDME9mGmfCnrNne4'
access_token = '780304879227052032-JAtPkXPwZcksCXjghnPrplYdUdorExr'
access_secret = '97ssbB6CDC5zjDFaAPIhsQPm4ZYZPLnuq7gyrmAnKEly0'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            print data
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
            print 'System sleeping 5 minutes'
            return True
        def on_error(self, status):
            print(status)
            return True
print "I am here1"
twitter_stream = Stream(auth, MyListener())
print "I am here2"
twitter_stream.filter(track=['#russia2018'])