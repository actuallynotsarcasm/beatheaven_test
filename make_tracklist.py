import requests, json, aiohttp, asyncio, time
from bs4 import BeautifulSoup
#from tqdm import tqdm
import tqdm
from functools import wraps


limit = 100
n_pages = 80

sem_limit = 500

class func_pbar:
    def __init__(self, target_iters, pbar=None):
        self.target_iters = target_iters
        self.start = False
        if not pbar:
            from tqdm import tqdm
            self.pbar = tqdm(total=target_iters, leave=False)
        else:
            self.pbar = pbar(total=target_iters, leave=False)
        self.pbar.clear()
        self.pbar.leave = True

    def __call__(self, fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            result = await fn(*args, **kwargs)
            self.pbar.update(1)
            return result
        return wrapper


@func_pbar(n_pages)
async def get_one_page(url, session):
    resp = await session.request('GET', url=url)
    data = await resp.json()
    return data


async def get_tracklist(country, api_key, limit, n_pages):
    async with aiohttp.ClientSession() as session:
        reqs = [get_one_page(f'http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country}&api_key={api_key}&format=json&limit={limit}&page={page}', session) for page in range(1, n_pages + 1)]
        resps = await asyncio.gather(*reqs)
    resps_lists = [resp['tracks']['track'] for resp in resps]
    all_tracks_info = sum(resps_lists, start=[])
    tracklist = [{'title': track['name'] + ' - ' + track['artist']['name'], 'url': track['url']} for track in all_tracks_info]
    return tracklist


@func_pbar(limit * n_pages)
async def get_youtube_url(url, session, semaphore):
    async with semaphore:
        try:
            resp = await session.request('GET', url=url)
            if resp.status == 200:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                obj = soup.find('a', attrs={'class': 'header-new-playlink', 'title': 'Play on YouTube'})
                if obj:
                    url = obj.attrs['href']
                    return url
                else:
                    return 'url not found'
            else:
                return await resp.text()
        except TimeoutError:
            return 'timeout'
    

async def parse_tracks(tracks, sem_limit):
    sem = asyncio.Semaphore(sem_limit)
    async with aiohttp.ClientSession() as session:
        reqs = [get_youtube_url(track['url'], session, sem) for track in tracks]
        urls = await asyncio.gather(*reqs)
    for i, url in enumerate(urls):
        tracks[i]['youtube'] = url
    return tracks


with open('creds_last_fm.json', 'r') as f:
    creds = json.load(f)

country = 'united states'

tracklist = asyncio.run(get_tracklist(country, creds['api_key'], limit, n_pages))
tracklist = asyncio.run(parse_tracks(tracklist, sem_limit))

with open('resp.json', 'w') as f:
    json.dump(tracklist, f, indent=4)