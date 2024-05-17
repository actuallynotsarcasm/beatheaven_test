import os
import json
import asyncio
import aiohttp

from tqdm import tqdm
from urllib.parse import unquote


class func_pbar:
    def __init__(self, target_iters, pbar=None):
        from functools import wraps
        self.wr = wraps
        self.target_iters = target_iters
        self.first_call = True
        self.pbar_func = pbar

    def init_pbar(self):
        if not self.pbar_func:
            from tqdm import tqdm
            self.pbar = tqdm(total=self.target_iters, leave=False)
        else:
            self.pbar = self.pbar_func(total=self.target_iters, leave=False)
    
    def __call__(self, fn):
        @self.wr(fn)
        async def async_wrapper(*args, **kwargs):
            if self.first_call:
                self.first_call = False
                self.init_pbar()
            result = await fn(*args, **kwargs)
            self.pbar.update(1)
            return result
        return async_wrapper


def replace_all(text, char_list):
    for char in char_list:
        text = text.replace(char, ' ').strip()
    return text


async def get_track_info(url, id, youtube_url, session, semaphore):
    async with semaphore:
        try:
            resp = await session.request('GET', url=url)
            data = await resp.json()
            #print('keys:')
            #print(data.keys())
            if 'track' not in data.keys():
                print('half failed url:')
                print(url)
                print(await resp.text())
                url += '&autocorrect=1'
                resp = await session.request('GET', url=url)
                data = await resp.json()
            if 'track' not in data.keys():
                print('failed url:')
                print(url)
                raise Exception()
            data['metadata'] = data['track']
            data['youtube_url'] = youtube_url
            data.pop('track')
            #print('success url:')
            #print(url)
            return id, data                
        except TimeoutError:
            return 'timeout'
        except Exception:
            print('errored url')
            print(url)
            raise Exception()
    

async def parse_metadata(tracks, api_key, sem_limit):
    sem = asyncio.Semaphore(sem_limit)
    pbar = func_pbar(len(tracks), tqdm)
    async with aiohttp.ClientSession() as session:
        reqs = []
        for track in tracks:
            id = track['id']
            artist = track['artist']
            name = track['name']
            youtube_url = track['youtube_url']
            url = f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={name}&format=json'
            reqs.append(pbar(get_track_info)(url, id, youtube_url, session, sem))
        tracks_data = await asyncio.gather(*reqs)
    metadata = {}
    for id, track_data in tracks_data:
        metadata[id] = track_data
    return metadata


music_dir = 'music'
file_list = os.listdir(music_dir)
title_list = list(map(lambda x: x[:-4], file_list))

with open('resp.json', 'r') as f:
    data = json.load(f)

chars = ['&', '\'', '#', '[', ']', ';']
track_ids = {}
tracks_for_search = []

for id, title in enumerate(tqdm(title_list)):
    found = False
    for item in data:
        if replace_all(item['title'], chars) == title:
            track_ids[title] = id
            found = True
            url = item['url']
            url = url.replace('https://www.last.fm/music/', '').replace('%25', '%').replace('&', '%26')
            artist, name = url.split('/_/')
            youtube_url = item['youtube']
            tracks_for_search.append({'name': name, 'artist': artist, 'youtube_url': youtube_url, 'id': id})
            break
    if not found:
        print('NOT FOUND')
        print(title)
        break

with open('creds_last_fm.json', 'r') as f:
    creds = json.load(f)

semaphore_limit = 3

metadata = asyncio.run(parse_metadata(tracks_for_search, creds['api_key'], semaphore_limit))

with open('music_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

with open('track_ids.json', 'w') as f:
    json.dump(track_ids, f, indent=4)