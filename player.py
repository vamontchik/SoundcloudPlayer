import requests
import vlc
from time import sleep

# read in sensitive information
with open('creds.txt', 'r') as f:
    CLIENT_ID = f.readline().strip().split(' = ')[1]
    CLIENT_SECRET = f.readline().strip().split(' = ')[1]

# constants
REQUEST_BASE = 'https://api.soundcloud.com/users/66931029/favorites'
CLIENT_URL_APPEND = 'client_id=' + CLIENT_ID
LIMIT = 300
LIMIT_APPEND = 'limit=' + str(LIMIT)
AND = '&'
START_QUERY = '?'

# perform query to obtain json object w/ titles & stream urls
request_query = REQUEST_BASE + START_QUERY + CLIENT_URL_APPEND + AND + LIMIT_APPEND
res = requests.get(request_query)
res_json = res.json()
song_titles = [song['title'] for song in res_json]

# cli
for i, song in enumerate(song_titles):
    print(str(i) + ": " + song)

while True:
    song_num = int(input('select song number: '))
    stream_url = res_json[song_num]['stream_url'] + START_QUERY + CLIENT_URL_APPEND

    p = vlc.MediaPlayer(stream_url)

    volume = int(input('volume: '))
    res = p.audio_set_volume(volume) 

    p.play()
    sleep(1.5) # time for it to start playing...

    def graphic_for_position(position):
        for i in range(1,50):
            if position < i/50:
                arrows = i * '>'
                dots = (50 - i) * '.'
                return '[' + arrows + dots + ']'
        return '[]'

    while p.is_playing():
        print(res_json[song_num]['title'] + ' --- ' + graphic_for_position(p.get_position()) + ' --- ' + str(p.get_position()), end='\r')