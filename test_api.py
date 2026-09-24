import urllib.request
import json

req = urllib.request.Request('http://localhost:5173/api/connect', method='POST')
req.add_header('Content-Type', 'application/json')
data = json.dumps({'url': 'libsql://test', 'token': 'test'}).encode('utf-8')
try:
    response = urllib.request.urlopen(req, data=data)
    print("Status:", response.status)
    print("Body:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode('utf-8'))
