from ytmusicapi import YTMusic
import ytmusicapi as yt
import json


def error_hook(obj):
    print(obj)
    return obj

ytmusic = YTMusic('oauth.json')

#resp = json.loads(str(ytmusic.get_charts(country='ZZ')), )
#resp = json.loads('{"a":"b","c":{"d":"e","f":id()}}', object_hook=error_hook)
resp = ytmusic.get_song('40JzyaOYJeY')

#print(list(list(resp.values())[1].values())[1][1]['videoId']())

with open('ytsearch.json', 'w') as f:
    json.dump(resp, indent=4, fp=f, )