import json
from hyper import HTTPConnection

conn = HTTPConnection('localhost:8080', secure=True)
conn.request('GET', '/')
resp = conn.get_response()
index_data = json.loads(resp.read().decode("utf8"))

for _id in index_data[:1000]:
    book_details_path = "/book?id={}".format(_id)
    request_id = conn.request('GET', book_details_path)
    if request_id:
        # we're using HTTP2
        response = conn.get_response(request_id)
    else:
        # we're using HTTP 1.1
        response = conn.get_response()

    print(response)
    body = json.loads(response.read().decode("utf8"))
    print(body)

