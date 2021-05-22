import requests
from io import BytesIO
import json
import time
import jsonify

file = open('test_data.txt', 'r')

url = 'http://127.0.0.1:5000/'
file_payload = {'file': file,
                'substring': 'ccttaactacggacgtttgt'}
start = time.time()
r = requests.post(url, files=file_payload)
stop = time.time()
print(r)
print(stop-start)
