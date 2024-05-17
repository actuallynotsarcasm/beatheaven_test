import json, pytube
from tqdm import tqdm

with open('resp.json', 'r') as f:
    tracklist = json.load(f)

for track in tqdm(tracklist):
    try:
        download = pytube.YouTube(track['youtube'])
        path = download.streams.get_audio_only().download(output_path='music_test', max_retries=5)
        print(path)
        assert False
    except Exception as e:
        tqdm.write(track['title']+': '+track['youtube'])
        print(e)