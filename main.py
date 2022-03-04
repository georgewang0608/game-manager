import urllib.request, urllib.error, urllib.parse, json, webbrowser
from flask import Flask, render_template, request

storeurl = "http://store.steampowered.com/api/"
steamurl = "https://api.steampowered.com/"
twitchurl = "https://api.twitch.tv/"


# Given method to make JSON more readable. Requires JSON object as parameter and returns a readable
# version of it to print
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


# Given method to check for errors on a given URL. Requires a URL and either returns an opened
# request to read it or None if it reaches an error
def safe_get(url):
    try:
        return urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


# Uses storefront API to access details about a particular game. Requires the game's appid
# and any desired filters (optional) as parameters and returns string of the json format.
def appdetails(appid, filters=''):
    params = {"appids": appid, "filters": filters}
    url = storeurl + "appdetails?" + urllib.parse.urlencode(params)
    safedata = safe_get(url)  # split this up in case invalid appid so we can get an error
    loadeddata = json.loads(safedata)  # why is this json.loads instead of json.load?
    return loadeddata


# Accesses personal Steam library by constructing url and returning a json file. Requires an
# authentication key and a Steam user's personal Steam ID. Can also exclude free games if desired.
# Temporarily commented out because we don't appear to be using it right now.
# def get_games(key, steamid, include_played_free_games=True, appids_filter=None):
#    combinedurl = steamurl + "IPlayerService/GetOwnedGames/v1/?key=" + key + "&steamid=" + \
#                  str(steamid) + "&include_appinfo=" + str(True) + "&nclude_played_free_games=" \
#                  + str(include_played_free_games) + "&appids_filter=" + str(appids_filter)
#    safedata = safe_get(combinedurl)
#    return json.load(safedata)

# Accesses user's history to check recent games played (default of 10 games) and returns a json file
# about those games' data.
def get_games_recent(key, steamid, count=10):
    combinedurl = steamurl + "IPlayerService/GetRecentlyPlayedGames/v1/?key=" + key + "&steamid=" \
                  + str(steamid) + "&count=" + str(count)
    safedata = safe_get(combinedurl)
    if safedata is None:
        return None
    else:
        return json.loads(safedata)


# Accesses a game's info to check the number of players currently online on a particular game,
# taking the game's appid as a parameter and return a json of the info. Temporarily commented out
# because we don't appear to be using it at the moment.
# def get_current_players(appid):
#    combinedurl = steamurl + "ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=" + str(appid)
#    safedata = safe_get(combinedurl)
#    return json.load(safedata)

# Searches for streams on Twitch using a search keyword (in our case, the name of a game), which
# is taken as a parameter. As of right now, no way to organize search results or check if stream is
# accurate. Currently returning list of 3 stream IDs for embedding onto site but can be changed.
def get_twitch_search(game):
    params = {"query": game}
    paramstr = urllib.parse.urlencode(params)
    url = twitchurl + "helix/search/categories?" + paramstr
    hdr = {'Client-ID': "10thxh1tgtgb7j2g4842qcgptipob4",
           'Authorization': "Bearer rmxafdqguk8gmu9h6jnl512zznpj3e"}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    response = response.read().decode('utf-8')
    streamdata = json.loads(response)
    #print(streamdata)
    #streamlist = []
    #for stream in streamdata["data"][0:1]:  # can fetch more/less than 3 streams if desired
    #print(streamdata["data"][0]["id"])
    if len(streamdata["data"]) > 0:
        params = {"broadcaster_id": streamdata["data"][0]["id"]}
        paramstr = urllib.parse.urlencode(params)
        channelurl = twitchurl + "helix/channels?" + paramstr
        channelreq = urllib.request.Request(channelurl, headers=hdr)
        channelresponse = urllib.request.urlopen(channelreq)
        channelresponse = channelresponse.read().decode('utf-8')
        channeldata = json.loads(channelresponse)
    #print(channeldata)
        if len(channeldata["data"]) > 0:
            return channeldata["data"][0]["broadcaster_name"]
        else:
            return None
    #return streamlist
    else: 
        return None 
#print(get_twitch_search("halo"))

# Takes in a genre/tag as a parameter to search the Steam featured section for any similar games
# and returns it as a dictionary.
def recommendation(genre):
    dic = {}
    url = storeurl + "featured/"
    data = json.loads(safe_get(url))
    dic = recommendation_helper(data, genre, dic, "large_capsules")
    dic = recommendation_helper(data, genre, dic, "featured_win")
    dic = recommendation_helper(data, genre, dic, "featured_mac")
    dic = recommendation_helper(data, genre, dic, "featured_linux")
    return dic


def recommendation_helper(data, genre, dic, OS):
    for x in data[OS]:
        appdetail = appdetails(x["id"])
        genres = appdetail[str(x["id"])]["data"]["genres"]
        for y in genres:
            if genre == y["description"]:
                dic[str(x["id"])] = {"name": x["name"], "genre": genre}
    return dic


# Takes in two dictionaries, one with a player's recently played games and another with any
# recommendations they've been given. Pulls news and stream data into dictionary separated by
# recent and recommended for return. This info should go directly onto our page.
def get_info(recentdict, recsdict):
    infodict = {"recent games": [], "recommended games": []}
    for game in recentdict["response"]["games"]:  # call must pass in recentdict with get_recent_games
        params = {"appid": game["appid"]}
        paramstr = urllib.parse.urlencode(params)
        combinedurl = steamurl + "ISteamNews/GetNewsForApp/v2/?" + paramstr + "&count=3"  # can add max length to content or count for # of posts
        safedata = safe_get(combinedurl)
        news = json.loads(safedata)
        streams = get_twitch_search(game["name"].replace(" ",""))
        #print(streams)
        infodict["recent games"].append({"name": game["name"],
                                         "news": news["appnews"]["newsitems"], "streams": streams})
    for gameid in recsdict.keys():
        combinedurl = steamurl + "ISteamNews/GetNewsForApp/v2/?appid=" + gameid  + "&count=3" # can add max length to content or count for # of posts
        safedata = safe_get(combinedurl)
        news = json.loads(safedata)
        streams = get_twitch_search(recsdict[gameid]["name"].replace(" ",""))
        infodict["recommended games"].append({"name": recsdict[gameid]["name"], "genrerec": recsdict[gameid]["genre"],
                                              "news": news["appnews"]["newsitems"],
                                              "streams": streams})
    return infodict


app = Flask(__name__)


@app.route('/')
def main_handler():
    return render_template('mainpage.html', page_title='Game Manager')


@app.route('/homepage')
def homepage_handler():
    username = request.args.get('username')
    if get_games_recent(steamid=username, key="BE8EB884D291A5695FE1093BA30C3E93") is None:
        return render_template('mainpage.html', page_title='mainpage - Error',
                               prompt='The steam ID is invalid')
    elif len(get_games_recent(steamid=username, key="BE8EB884D291A5695FE1093BA30C3E93")["response"].keys()) == 0:
        return render_template('mainpage.html', page_title='mainpage - Error',
                               prompt='The steam ID is private please set it to pulic and try again!')
    else:
        recentdic = get_games_recent(steamid=username, key="BE8EB884D291A5695FE1093BA30C3E93")
        favorite_genre = {}
        if len(recentdic["response"]) > 1:
            for x in recentdic["response"]["games"]:
                genre = appdetails(x["appid"])[str(x["appid"])]["data"]["genres"]
                for y in range(len(genre)):         
                    if genre[y]["description"] in favorite_genre.keys():
                        favorite_genre[genre[y]["description"]] += 1
                    else:
                        favorite_genre[genre[y]["description"]] = 1
            max_key = max(favorite_genre, key=favorite_genre.get)
            if max_key is not None:
                recsdict = recommendation(max_key)
            else:
                max_key = sorted((x for x in favorite_genre.keys()), key = lambda x: favorite_genre[x], reverse = True)
                recsdict = recommendation(max_key[0])
                #print(recsdict)
            everything = get_info(recentdic, recsdict)
            stream = []
            stream2 = []
            news = []
            for x in everything["recommended games"]:
                if x["streams"] is not None:
                    stream.append(x["streams"])
                if x["news"] is not None:
                    for y in x["news"]:
                        news.append(y["title"])    
                        news.append(y["url"])
            for x in everything["recent games"]:
                if x["streams"] is not None:
                    stream2.append(x["streams"])
                if x["news"] is not None:
                    for y in x["news"]:
                        news.append(y["title"])
                        news.append(y["url"])
            return render_template('homepage.html', page_title='homepage',
                                name=username, news=news, length=range(0, len(news), 2), stream=stream,
                                stream2=stream2, genre=max_key)
        else:
            return render_template('mainpage.html', page_title='mainpage - Error',
                               prompt='You have not played any steam games recently, we have nothing to update you:(')


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)