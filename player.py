import requests
import vlc
from time import sleep

with open('creds.txt', 'r') as f:
    CLIENT_ID = f.readline().strip()
    CLIENT_SECRET = f.readline().strip()

REQUEST_RESOLVE_BASE = 'https://api.soundcloud.com/resolve'
REQUEST_URL = 'url=https://soundcloud.com/woofsalot/likes'
CLIENT_URL_APPEND = 'client_id=' + CLIENT_ID
AND = '&'
START_QUERY = '?'

res = requests.get(REQUEST_RESOLVE_BASE + START_QUERY + REQUEST_URL + AND + CLIENT_URL_APPEND)
res_json = res.json()

# import json
# print(json.dumps(res.json()[0], indent=2))

print('streamable: ' + str(res_json[0]['streamable']))

stream_url = res_json[0]['stream_url'] + START_QUERY + CLIENT_URL_APPEND
print('stream_url: ' + stream_url)

p = vlc.MediaPlayer(stream_url)
p.play()

sleep(5)
while p.is_playing():
    sleep(1)