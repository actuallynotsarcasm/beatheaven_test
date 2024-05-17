import requests, json, aiohttp, asyncio, time, tqdm
from normalize_json import normalize


def check_video(release):
    if 'videos' in release:
        return release['videos'][0]['uri']
    elif 'message' in release:
        return release['message']
    return ''


async def get_url(url, session):
    resp = await session.request('GET', url=url)
    data = await resp.json()
    return data


async def parse_resp(resp, timeout=2):
    tracks = [track['title'] for track in resp['results']]
    urls = [track['resource_url'] for track in resp['results']]
    async with aiohttp.ClientSession() as session:
        reqs = []
        for url in urls:
            reqs.append(get_url(url, session))
            time.sleep(1)
        releases = await asyncio.gather(*reqs)
    videos = list(map(check_video, releases))
    resp = {track[0]: track[1] for track in zip(tracks, videos)}
    return resp


def parse_resp_sync(resp, timeout=2):
    tracks = [track['title'] for track in resp['results']]
    urls = [track['resource_url'] for track in resp['results']]
    releases = []
    for url in tqdm.tqdm(urls):
        releases.append(requests.get(url).json())
        time.sleep(2)
    #releases = [requests.get(url).json() for url in tqdm.tqdm(urls)]
    videos = list(map(check_video, releases))
    resp = {track[0]: track[1] for track in zip(tracks, videos)}
    return resp


with open('user_token.json', 'r') as f:
    user_token = json.load(f)

page = 1
per_page = 50

resp = requests.get(url=f"https://api.discogs.com/database/search?type=master&page={page}&per_page={per_page}",
                    headers={
                        "Authorization": f"Discogs token={user_token['user_token']}"
                    })

with open('resp.json', 'w') as f:
    f.write(normalize(resp.text))

with open('resp.json', 'r') as f:
    resp = json.load(f)

timeout = 2

#resp = asyncio.run(parse_resp(resp, timeout=timeout))
resp = parse_resp_sync(resp)

with open('resp.json', 'w') as f:
    f.write(json.dumps(resp, indent=4))