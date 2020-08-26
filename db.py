import sqlite3, requests

conn = sqlite3.connect('twitter_resources.db', check_same_thread=False)
c = conn.cursor()

def setup_db():
    c.execute("""CREATE TABLE IF NOT EXISTS teams_twitter (
            id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL UNIQUE,
            twitter_handle TEXT NOT NULL UNIQUE,
            hashtag TEXT NOT NULL UNIQUE,
            season INTEGER NOT NULL,
            tricode TEXT UNIQUE)
            """)

    conn.commit()

    data = ["Anaheim Ducks, @AnaheimDucks, #LetsGoDucks",
            "Arizona Coyotes, @ArizonaCoyotes, #Yotes",
            "Boston Bruins, @NHLBruins, #NHLBruins",
            "Buffalo Sabres, @BuffaloSabres, #Sabres50",
            "Calgary Flames, @NHLFlames, #Flames",
            "Carolina Hurricanes, @NHLCanes, #LetsGoCanes",
            "Chicago Blackhawks, @NHLBlackhawks, #Blackhawks",
            "Colorado Avalanche, @Avalanche, #GoAvsGo",
            "Columbus Blue Jackets, @BlueJacketsNHL, #CBJ",
            "Dallas Stars, @DallasStars, #GoStars",
            "Detroit Red Wings, @DetroitRedWings, #LGRW",
            "Edmonton Oilers, @EdmontonOilers, #LetsGoOilers",
            "Florida Panthers, @FlaPanthers, #FlaPanthers",
            "Los Angeles Kings, @LAKings, #GoKingsGo",
            "Minnesota Wild, @mnwild, #MNWild",
            "Montreal Canadiens, @CanadiensMTL, #GoHabsGo",
            "Nashville Predators, @PredsNHL, #Preds",
            "New Jersey Devils, @NJDevils, #NJDevils",
            "New York Islanders, @NYIslanders, #Isles",
            "New York Rangers, @NYRangers, #PlayLikeANewYorker",
            "Ottawa Senators, @Senators, #goSensgo",
            "Philadelphia Flyers, @NHLFlyers, #FlyOrDie",
            "Pittsburgh Penguins, @penguins, #LetsGoPens",
            "San Jose Sharks, @SanJoseSharks, #SJSharks",
            "St. Louis Blues, @StLouisBlues, #STLBlues",
            "Tampa Bay Lightning, @TBLightning, #GoBolts",
            "Toronto Maple Leafs, @MapleLeafs, #LeafsForever",
            "Vancouver Canucks, @Canucks, #Canucks",
            "Vegas Golden Knights, @GoldenKnights, #VegasBorn",
            "Washington Capitals, @Capitals, #ALLCAPS",
            "Winnipeg Jets, @NHLJets, #GoJetsGo"]

    for team in data:
        name, handle, hashtag = team.split(",")
        handle = handle.strip()
        hashtag = hashtag.strip()

    c.execute("INSERT INTO teams_twitter (team_name, twitter_handle, hashtag, season) VALUES ('{}', '{}', '{}', 2019)".format(name, handle, hashtag))
    conn.commit()

def update_db_with_tricodes():
    r = requests.get("https://statsapi.web.nhl.com//api/v1/teams")
    teams = r.json()["teams"]

    for team in teams:
        teamname = team.get("name")
        tricode = team.get("abbreviation")
        print(tricode, teamname)

        c.execute("""UPDATE teams_twitter
                    SET tricode = "{}"
                    WHERE team_name = '{}'""".format(tricode, teamname))

        conn.commit()

def get_hashtags(*teams):
    results = []
    for team in teams:
        c.execute("SELECT hashtag FROM teams_twitter WHERE team_name='{}'".format(team))
        results.append(*c.fetchone())
    return results

def get_tricodes(*teams):
    results = []
    for team in teams:
        c.execute("SELECT tricode FROM teams_twitter WHERE team_name='{}'".format(team))
        results.append(*c.fetchone())
    return results