import datetime
import time
import results_parser
import tweepy
import os
import sqlite3
import json

conn = sqlite3.connect('twitter_resources.db', check_same_thread=False)
c = conn.cursor()

API_key = os.environ.get("API_key")
API_secret_key = os.environ.get("API_secret_key")
Access_token = os.environ.get("Access_token")
Access_token_secret = os.environ.get("Access_token_secret")


def tweet_result(tweets):

    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(Access_token, Access_token_secret)

    api = tweepy.API(auth)
    reply_to = ""
    for tweet in tweets:
        print(tweet)
        reply_to = api.update_status(tweet, in_reply_to_status_id=reply_to).id
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

    try:
        c.execute(
            """INSERT INTO unfinished (Date, Games) VALUES ('{}', '{}')""".format(date, json.dumps(games)))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    check_unfinished(date)


def check_unfinished(date):
    c.execute("SELECT Games FROM unfinished WHERE Date='{}'".format(date))
    search_result = c.fetchone()
    if search_result:
        games = json.loads(search_result[0])
        while set(games["tweeted"]) != set(games["all"]):
            data = results_parser.return_todays_data(date)
            for game in data:
                if data[game].get("finished") and game not in games["tweeted"]:
                    games["finished"].append(game)
                    tweet_result(data[game]["tweets"])
                    games["tweeted"].append(game)

            c.execute("""UPDATE unfinished SET Games = '{}' WHERE Date = '{}'""".format(json.dumps(games), date))
            conn.commit()
            print(games)
            time.sleep(600)

        c.execute("DELETE FROM unfinished WHERE Date='{}'".format(date))
        conn.commit()
    else:
        pass


def run():
    gather_tweets()


if __name__ == "__main__":
    run()
