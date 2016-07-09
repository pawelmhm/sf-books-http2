import json
import sys

from OpenSSL import SSL
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log

def load_stock():
    with open("books.json") as stock_file:
        return json.load(stock_file)

BOOKS = load_stock()


class Index(Resource):
    def render_GET(self, request):
        return json.dumps(list(BOOKS.keys())).encode("utf8")


class Book(Resource):
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


    class MyContextFactory(DefaultOpenSSLContextFactory):
        # Context subclass to allow manipulating some context settings (e.g. cipher selection).
        def cacheContext(self):
            if self._context is None:
                ctx = self._contextFactory(self.sslmethod)
                ctx.set_options(SSL.OP_NO_SSLv2)
                ctx.use_certificate_file(self.certificateFileName)
                ctx.use_privatekey_file(self.privateKeyFileName)
                # will this help?
                #ctx.set_cipher_list("ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256")
                # ctx.set_cipher_list("ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS")
                self._context = ctx

    # https://github.com/icing/mod_h2/issues/25
    # ERR_SPDY_INADEQUATE_TRANSPORT_SECURITY
    context_factory = MyContextFactory("key.pem", "cert.pem")
    reactor.listenSSL(8080, site, context_factory)
    reactor.run()
