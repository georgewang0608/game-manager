import urllib.request
import json
url = "https://api.twitch.tv/helix/search/categories?query=testing"
hdr = { 'Client-ID' : "10thxh1tgtgb7j2g4842qcgptipob4", 'Authorization' : "Bearer rmxafdqguk8gmu9h6jnl512zznpj3e"}

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

req = urllib.request.Request(url, headers=hdr)
response = urllib.request.urlopen(req)
response = response.read().decode('utf-8')
data = json.loads(response)
print(pretty(data))

# print(response.read())