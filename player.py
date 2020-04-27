import requests
import vlc
import datetime
import os
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
song_titles = [song['user']['username'] + ' - ' + song['title'] for song in res_json]

# cli
for i, song in enumerate(song_titles):
    print(str(i) + ": " + song)

while True:
    user_input = input('player> ')
    if user_input == 'quit':
        break

    song_num = int(user_input)
    stream_url = res_json[song_num]['stream_url'] + START_QUERY + CLIENT_URL_APPEND

    p = vlc.MediaPlayer(stream_url)

    volume = int(input('volume: '))
    res = p.audio_set_volume(volume)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # https://stackoverflow.com/a/978264 - to redirect prefetch err message from vlc :)
    def turn_off_stdout_and_stderr():
        null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        save = os.dup(1), os.dup(2)
        os.dup2(null_fds[0], 1)
        os.dup2(null_fds[1], 2)
        return null_fds, save
    
    def turn_on_stdout_and_stderr(null_fds, save):
        os.dup2(save[0], 1)
        os.dup2(save[1], 2)
        os.close(null_fds[0])
        os.close(null_fds[1])
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    null_fds, save = turn_off_stdout_and_stderr()
    p.play()
    sleep(1.5) # time for it to start playing & swallow prefetch error msg
    turn_on_stdout_and_stderr(null_fds, save)

    def graphic_for_position(position):
        for i in range(1,50):
            if position < i/50:
                arrows = i * '>'
                dots = (50 - i) * '.'
                return '[' + arrows + dots + ']'
        return '[' + 50 * '>' + ']'

    def get_time_mm_ss(time_in_ms):
        return datetime.datetime.fromtimestamp(time_in_ms / 1000).strftime('%M:%S')

    while p.is_playing():
        print(res_json[song_num]['user']['username'] + ' - ' + res_json[song_num]['title'] + ' ' + \
              graphic_for_position(p.get_position()) + ' ' + \
              get_time_mm_ss(p.get_time()), end='\r')
    print() # to put input query on next line