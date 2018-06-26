import time
import csv
import sys
import tweepy
from tweepy.auth import OAuthHandler

reload(sys)
sys.setdefaultencoding('utf8')

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

# In this example, the handler is time.sleep(15 * 60)
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('System sleeping')
            time.sleep(15 * 60)
            continue
        except tweepy.TweepError:
            print('System sleeping')
            time.sleep(15 * 60)
        except StopIteration:
            break

# Open a new csv file with title row            
f = csv.writer(open('followers_JML.csv', 'wb'))
f.writerow(["ScreenName", "Name", "Location","Followers"])

# followers = tweepy.Cursor(api.followers,id="JoMaloneLondon").items()
# for follower in followers:
for follower in limit_handled(tweepy.Cursor(api.followers, id="JoMaloneLondon").items()):
    if follower.friends_count > 300:
        screenName = follower.screen_name.encode("utf-8")
        name = follower.name.encode("utf-8")
        location = follower.location.encode("utf-8")
        fcounts = follower.followers_count
        print(screenName,name,location,fcounts) 
        f.writerow([screenName,name,location,fcounts])
f.close()    

