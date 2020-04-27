import requests
import vlc
from time import sleep

with open('creds.txt', 'r') as f:
    CLIENT_ID = f.readline().strip().split(' = ')[1]
    CLIENT_SECRET = f.readline().strip().split(' = ')[1]

REQUEST_RESOLVE_BASE = 'https://api.soundcloud.com/resolve'
REQUEST_URL = 'url=https://soundcloud.com/woofsalot/likes'
CLIENT_URL_APPEND = 'client_id=' + CLIENT_ID
AND = '&'
START_QUERY = '?'

request_query = REQUEST_RESOLVE_BASE + START_QUERY + REQUEST_URL + AND + CLIENT_URL_APPEND
res = requests.get(request_query)
res_json = res.json()
song_titles = [song['title'] for song in res_json]

def select_song(song_list):
    for i, song in enumerate(song_list):
        print(str(i) + ": " + song)
    return int(input('select song number: '))

while True:
    song_num = select_song(song_titles)
    stream_url = res_json[song_num]['stream_url'] + START_QUERY + CLIENT_URL_APPEND

    p = vlc.MediaPlayer(stream_url)

    volume = int(input('volume: '))
    res = p.audio_set_volume(volume) # 0 = muted, 100 = 0 db (default of 99 ... lol)

    p.play()
    sleep(5) # time for it to start playing...

    interrupted = False
    while p.is_playing():
        query_during_song = input('stop: ')
        if query_during_song == 'y':
            p.stop()
            break
