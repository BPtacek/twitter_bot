import db
import nhl_api_calls


# parsing the api call response into two main dicts: dates and games. Dates contains dates, games contains teams,
# their season record, status, gameid, score if game already played/in progress
def parse_strings_for_tweets(data):
    dates = {}
    games = {}
    for date in data["dates"]:
        dates.setdefault(str(len(dates)), date["date"])
        games[date["date"]] = {}
        for game in date["games"]:
            home = game["teams"]["home"]["team"]["name"]
            away = game["teams"]["away"]["team"]["name"]
            opponents = "{} - {}".format(home, away)
            tricodes = "{} - {}".format(*db.get_tricodes(home, away))
            gameid = game["link"].lstrip('/api/v1/')
            status = game["status"]["detailedState"]
            czechs = get_czechs_and_slovaks(gameid)
            hashtags = db.get_hashtags(home, away)

            if status == "Final":
                score = "{} : {}".format(game["teams"]["home"]["score"], game["teams"]["away"]["score"])
            else:
                score = "- : -"

            games[date["date"]].setdefault(str(len(games[date["date"]])),
                                           {"opponents": opponents, "status": status, "hashtags": " ".join(hashtags),
                                            "gameid": gameid, "tricodes": tricodes, "score": score, "czechs": czechs})
    return dates, games


def get_czechs_and_slovaks(gameid):
    basic_game_data = nhl_api_calls.make_call(gameid)
    skaters = basic_game_data["gameData"]["players"]
    players_stats = basic_game_data.get("liveData").get("boxscore").get("teams")
    stats_extracted = players_stats.get("away").get("players")
    stats_extracted.update(players_stats.get("home").get("players"))
    czechs = []
    for player in skaters:
        if skaters[player].get("nationality") in ("CZE", "SVK"):
            name, code = skaters[player]["fullName"], skaters[player]["currentTeam"].get("triCode", "???")
            if stats_extracted.get(player).get("position").get("code") == "G":
                stats = stats_extracted.get(player).get("stats").get("goalieStats")
                czechs.extend([" ".join(
                    [code, name, str(stats.get('timeOnIce')), str(stats.get("saves")) + " saves",
                     str(stats.get("savePercentage"))[:5] + "%"])])
            else:
                stats = stats_extracted.get(player).get("stats").get("skaterStats", {})
                if stats:
                    czechs.extend([" ".join([code, name, str(stats.get("timeOnIce", "??:??")),
                                             str(stats.get("goals", "0")) + "+" + str(stats.get("assists", "0")),
                                             str(stats.get("plusMinus", "0"))])])
    if not czechs:
        czechs = ["No CZE/SVK players involved"]

    return czechs


# function that prints out to the stdout collected and parsed search results
def create_tweets(raw_api_data):
    schedule = parse_strings_for_tweets(raw_api_data)
    if not schedule[0].get("0", None):
        return {}
    playday = schedule[0]["0"]
    gamedate = schedule[1][playday]
    tweets = {}
    for game in range(len(gamedate)):
        finished_game = True if gamedate[str(game)]["status"] in ("Final", "Cancelled", "Postponed") else False
        tweets[gamedate[str(game)]["opponents"]] = {"tweets": [], "finished": finished_game}
        opponents = gamedate[str(game)]["opponents"]
        hashtags = gamedate[str(game)]["hashtags"]
        tricodes = gamedate[str(game)]["tricodes"]
        base = playday + "\n" + opponents + " " + gamedate[str(game)]["score"] + "\n"
        tweet = base
        if gamedate[str(game)]["status"] in ("Cancelled", "Postponed"):
            tweet += "\n" + "Game " + gamedate[str(game)]["status"] + "\n\n" + hashtags
            tweets[opponents]["tweets"].append(tweet)
            continue

        for player in sorted(gamedate[str(game)]["czechs"]):
            meta = tweet + "\n" + player

            if len(meta) < 280:
                tweet = meta
                continue
            else:
                tweet = resolve_tweet_length(tweet, opponents, tricodes, hashtags)
                tweets[opponents]["tweets"].append(tweet)
                tweet = base + "\n" + player

        tweet = resolve_tweet_length(tweet, opponents, tricodes, hashtags)
        tweets[opponents]["tweets"].append(tweet)

    return tweets


def resolve_tweet_length(tweet, opponents, tricodes, hashtags):
    meta = tweet + "\n\n" + hashtags

    if len(meta) < 280:
        return meta
    else:
        meta = meta.replace(opponents, tricodes)
        if len(meta) < 280:
            return meta
        else:
            meta = tweet.replace(opponents, tricodes)
            if len(meta) < 280:
                return meta
            return tweet


# function to run the api call and collecting the result
def fetch_data(customdate=""):
    text = nhl_api_calls.make_call("schedule", customdate)
    return text


# main function running the whole thing
def return_todays_data(customdate=""):
    tweets = create_tweets(fetch_data(customdate))
    return tweets


if __name__ == "__main__":
    return_todays_data()
