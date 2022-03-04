import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.parse, urllib.request, urllib.error, json
# from flask import Flask, render_template

baseurl = "https://api.steampowered.com/"

# From HW6
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# From HW6
def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

# Accesses personal Steam library by constructing url and returning a json file. Requires an
# authentication key and a Steam user's personal Steam ID. Can also exclude free games if desired.
def get_games(key, steamid, include_played_free_games=True, appids_filter=None):
    combinedurl = baseurl + "IPlayerService/GetOwnedGames/v1/?key=" + key + "&steamid=" + \
                  str(steamid) + "&include_appinfo=" + str(True) + "&nclude_played_free_games=" \
                  + str(include_played_free_games) + "&appids_filter=" + str(appids_filter)
    return json.load(safe_get(combinedurl)) # split in case there's a None (if statement)

def get_games_recent(key, steamid, count=10):
    combinedurl = baseurl + "IPlayerService/GetRecentlyPlayedGames/v1/?key=" + key + "&steamid="\
                  + str(steamid) + "count=" + str(count)
    return json.load(safe_get(combinedurl))

def get_current_players(appid):
    combinedurl = baseurl + "ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=" + str(appid)
    return json.load(safe_get(combinedurl))

print(pretty(get_games_recent("BE8EB884D291A5695FE1093BA30C3E93", 76561198982122659)))  #method test

# Evaluates Steam library returned from get_games() and processes the information. Builds a
# backlog list (backlog referring to unplayed games someone's "going to play one of these day
# but never really does wink wink") and prints out a statement with how many games are in it.
# Then, it returns the backlog list.
#def evaluate_games(key, steamid, include_played_free_games=True, appids_filter=None):
#    try:
#        gamedict = get_games(key, steamid, include_played_free_games, appids_filter)
#        backlog = []
#        for game in gamedict["response"]["games"]:
#            if game["playtime_windows_forever"] == 0 and game["playtime_mac_forever"] == 0 and game["playtime_linux_forever"] == 0:
#                backlog.append(game["name"])
#        if len(backlog) == 0:
#            print("This user's backlog is empty. Nice!")
#        else:
#            print("This user has " + str(len(backlog)) + " unplayed games in their backlog!")
#        return backlog
#    except urllib.error.HTTPError as message:
#        print("There was an error processing the information.", message)
#    except urllib.error.URLError as message:
#        print("Error trying to reach server.", message)
#    return None

# app = Flask(__name__)

# @app.route("/")
# def structure():
#     return render_template()  # throw some stuff in here later
# if __name__ == "__main__":
#     app.run(host="localhost", port=8080, debug=True)