import sys

from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log

from twisted.internet import endpoints


class Index(Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"hello world (in HTTP2)"


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    site = server.Site(Index())
    endpoint_spec = "ssl:port=8080:privateKey=key.pem:extraCertChain=cert.pem"
    server = endpoints.serverFromString(reactor, endpoint_spec)
    server.listen(site)
    reactor.run()
