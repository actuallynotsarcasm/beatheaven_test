import requests
from fp.fp import FreeProxy

proxy_url = FreeProxy(https=True).get()

print(proxy_url)

proxies = {
    'http': proxy_url,
    'https': proxy_url
}
resp = requests.get('https://www.youtube.com/watch?v=oIIxlgcuQRU', proxies=proxies)

with open('proxy_resp.html', 'wb') as f:
    f.write(resp.text.encode(resp.encoding))