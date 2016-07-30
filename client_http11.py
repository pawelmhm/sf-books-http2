import json
import requests

s = requests.Session()
url = 'https://localhost:8080'
resp = s.get(url, verify="cert.pem")
index_data = json.loads(resp.text)

responses = []

for _id in index_data:
    book_details_path = "/book?id={}".format(_id)
    response = s.get(url + book_details_path, verify="cert.pem")
    body = json.loads(response.text)
    responses.append(body)

assert len(responses) == 3000
