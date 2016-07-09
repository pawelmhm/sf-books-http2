## Hello world in HTTP2 with Twisted

Trying to create sample Twisted web resource in HTTP2 that will work in Chrome. Chrome above 51 dropped
support for NPN. It only allows ALPN TLS extension. ALPN requires OpenSSL above 1.0.2 which is installed
by default only in Ubuntu. 

https://www.nginx.com/blog/supporting-http2-google-chrome-users/
https://ma.ttias.be/day-google-chrome-disables-http2-nearly-everyone-may-31st-2016/

## Note 

Certificate files are fake self signed certificates. If you'd like to test server with your clients you need
to add certificates to your OS certificate store (or pass certificate file to client somehow, e.g. using curl
cacert option.