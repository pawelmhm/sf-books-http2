import json
import sys

from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log

from twisted.internet import endpoints


def load_stock():
    # load data from JSON
    with open("books.json") as stock_file:
        return json.load(stock_file)

BOOKS = load_stock()


class Index(Resource):
    """Serve all book ids.
    """
    def render_GET(self, request):
        return json.dumps(list(BOOKS.keys())).encode("utf8")


class Book(Resource):
    """Return detailed data about each book.
    """
    isLeaf = True

    def render_GET(self, request):
        book_id = request.args.get(b"id")
        book = BOOKS.get(book_id[0].decode("utf8"))
        if not book:
            request.setResponseCode(404)
            return b""
        return json.dumps(book).encode("utf8")


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    root = Resource()
    root.putChild(b"", Index())
    root.putChild(b"book", Book())
    site = server.Site(root)
    endpoint_spec = "ssl:port=8080:privateKey=key.pem:extraCertChain=cert.pem"
    server = endpoints.serverFromString(reactor, endpoint_spec)
    server.listen(site)
    reactor.run()
