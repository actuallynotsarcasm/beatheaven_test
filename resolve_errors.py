import os, json

with open('resp.json', 'r') as f:
    tracklist = json.load(f)

music_listed = set(map(lambda x: x['title']+'.mp3', tracklist))
music_downloaded = set(os.listdir("music"))
#music_downloaded_errors = list(filter(lambda x: not('.mp3' in x), music_downloaded))
#music_missed = list(music_downloaded - music_listed)
#music_missed_fixed = [list(filter(lambda x: track in x, list(map(lambda x: x[:-4], music_listed))))[0] for\
#                      track in list(map(lambda x: x[:-4], music_missed))]
#resp_to_fix = list(filter(lambda x: x['title']+'.mp3' in music_missed, tracklist))
#errors = list(filter(lambda x: x[0] == ' ', music_downloaded))
fixed = list(map(lambda x: x[:-3]+'mp4', music_downloaded))
#[os.remove('music/'+fp) for fp in music_missed]
#with open('resp_to_fix.json', 'w') as f:
#    json.dump(resp_to_fix, f, indent=4)

#print(music_missed_fixed)
[os.rename('music/'+src, 'music/'+dst) for src, dst in zip(music_downloaded, fixed)]