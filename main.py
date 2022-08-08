import pyjokes
import api
import util
from time import sleep
import pyjokes
import getpass
import http.client
http.client.HTTPConnection.debuglevel = 5
 

class CLIClient:
    def __init__(self) -> None:
        self.token = None 
        self.tweets = None 



    def login(self):
        username = input("username : ")
        password = getpass.getpass("password : ")
        self.token=api.login("elon","tesla")
    
    def get_tweets(self):
        tweets = api.get_tweets(self.token)
        for tweet in tweets:
            print("({}) {} tweeted at {}".format(tweet['id'],tweet['author']['username'],tweet['created_at']))
            print(tweet['text'])
            print()
        
        temp = {}
        for tweet in tweets:
            text = tweet['text']
            tweet_id = tweet['id']
    
            if text in temp:
                temp[text] = max(tweet_id,temp[text])
            else:
                temp[text] = tweet_id
    
        tweets = [ (y,x) for x,y in temp.items()]
        tweets = sorted(tweets,reverse=True)
        self.tweets = tweets
    
    
    def make_joke(self):
        while True:
            joke = pyjokes.get_joke()
            if joke not in self.tweets:
                result = api.create_tweets(self.token,joke)
                self.tweets = [joke]+self.tweets[:-1]
                return result
    
    def make_jokes(self):
        print("posting jokes:")
        for _ in range(10):
            result = self.make_joke()
            print(result['text'])
            print()
            sleep(30)


           

def main():
    client = CLIClient()
    client.login() 
    client.get_tweets()
    client.make_jokes()
    

if __name__ == '__main__':
    main()
