import requests
import json

r = requests.get('http://127.0.0.1:8000/rest/post/5/')
print(r.text)

r = requests.put('http://127.0.0.1:8000/rest/post/5/',
                 data=json.dumps({'direction': 'From University to home',
                       'time': '03:00:01'}))
print(r.text)
