import datetime
import time
import results_parser
import tweepy
import os

API_key = os.environ.get("API_key")
API_secret_key = os.environ.get("API_secret_key")
Access_token = os.environ.get("Access_token")
Access_token_secret = os.environ.get("Access_token_secret")


def tweet_result(tweets):

    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(Access_token, Access_token_secret)

    api = tweepy.API(auth)

    for tweet in tweets:
        print(tweet)
        api.update_status(tweet)
        time.sleep(15)


def gather_tweets():
    date = str(datetime.date.today())
    data = results_parser.return_todays_data()
    games = {"finished": [], "tweeted": [], "all": list(data.keys())}
    for game in data:
        if data[game].get("finished"):
            games["finished"].append(game)
            tweet_result(data[game]["tweets"])
            games["tweeted"].append(game)

    while set(games["tweeted"]) != set(games["all"]):
        data = results_parser.return_todays_data(date)
        for game in data:
            if data[game].get("finished") and game not in games["tweeted"]:
                games["finished"].append(game)
                tweet_result(data[game]["tweets"])
                games["tweeted"].append(game)
        print(games)
        time.sleep(600)

def run():
    gather_tweets()
