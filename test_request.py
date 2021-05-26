import requests
from io import BytesIO
import json

file = open('test_data.txt', 'r')

url = 'https://fm-index.herokuapp.com/preloaded'
marker = 1 # should be between 1-2 inclusive
substring = 'AAATAATTAATATT'
payload = {
            'marker': marker,
            'substring': substring
          }

r = requests.post(url, files=file_payload)

print(r.json())
