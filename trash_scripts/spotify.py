'''
with open('access_token_spotify.json', 'r') as f:
    access_token = json.load(f)


resp = requests.get(url="https://api.spotify.com/v1/tracks/6Oc3feguq7XYfUXjGjlbzz?market=ES",
                    headers={"Authorization": f"Bearer {access_token['access_token']}"})
'''