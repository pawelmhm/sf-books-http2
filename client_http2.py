import json
from hyper import HTTPConnection

conn = HTTPConnection('localhost:8080', secure=True)
conn.request('GET', '/')
resp = conn.get_response()

# process initial page with book ids
index_data = json.loads(resp.read().decode("utf8"))

responses = []
chunk_size = 100

# split initial set of urls into chunks of 100 items
for i in range(0, len(index_data), chunk_size):
    request_ids = []

    # make requests
    for _id in index_data[i:i+chunk_size]:
        book_details_path = "/book?id={}".format(_id)
        request_id = conn.request('GET', book_details_path)
        request_ids.append(request_id)

    # get responses
    for req_id in request_ids:
        response = conn.get_response(req_id)
        body = json.loads(response.read().decode("utf8"))
        responses.append(body)

assert len(responses) == 3000
