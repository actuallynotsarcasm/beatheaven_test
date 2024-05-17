import requests, json
filename = 'background_noise/noise_2.wav'
file = open(filename, 'rb')
response = requests.post('http://localhost:8000/find_similar', files={'file': file})
songs = json.loads(response.text)
with open('track_resp.json', 'w') as f:
    f.write(response.text)
print(json.loads(response.text)['result'], sep='\n')