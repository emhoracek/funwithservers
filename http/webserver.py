#!/usr/bin/python
import socket
import sys

# from Python for hackers video
# IDEAs:
#       use python3
#       import logging and use logging.info instead of print >>sys.error
#       give the real date and stuff
#       find out how HTTP works
#       make Content-Length automatic
#       put the HTML in a different file/folder

#config constants
CFG_SRV_BIND_IF = "localhost"
CFG_SRV_BIND_PORT = 8000
CFG_SRV_LISTEN_BACKLOG = 10
# end config

#Header fields
connection = "" # control options for current connection -- removed by proxies or gateways
#either content-length OR transfer-encoding
content-length = ""
transfer-encoding = "" # e.g. gzip, chunked
host = "" # required
te = "" # acceptable transfer encodings in response
trailer = "" # integrity check blah?
upgrade = "" # transitioning protocols?
via = "" #intermediate protocols³


# canned HTTP response (mimicing Apache response)
# This is kinda evil???? ]:)
HTTP_RESPONSE = """HTTP/1.1 200 OK
Date: Tue, 3 March 2015 03:22:00 EST
Server: Apache/2.2.17 (Unix) mod_ssl/2.2.16 OpenSSL/0.9.81 DAV/2
Last-Modified: Sat, 28 Aug 2010 22:17:02 GMT
ETag: "20e2b8b-3c-48ee99731f380"
Accept-Ranges: bytes
Connent-Length: 49
Connection: close
Conent-Type: text/html

<html><body><h1>Hello, world!</h1></body></html>
"""
# af_inet? sock_stream?
# Create a TCP/IP socket to listen on
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent "address already in use" error on server restart
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to port 8081 on all interfaces
# interfaces?
server_address = (CFG_SRV_BIND_IF, CFG_SRV_BIND_PORT)

#python3
print("our URL is http://localhost:%d/" % server_address[1], file=sys.stderr)
print("we can only be stopped by CTRL+C", file=sys.stderr)

server.bind(server_address)

# Listen for connections
server.listen(CFG_SRV_LISTEN_BACKLOG)

while True:
    try:
        # Wait for one incoming connection
        connection, client_address = server.accept()
        print("New connection from", client_address, file=sys.stderr)

        # Don't care what browser wants, just send response
        connection.send(bytearray(HTTP_RESPONSE, 'UTF-8'))
        print("Response sent.", file=sys.stderr)

        # Indicate going to disconnect
        connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
        
        # Close connection
        connection.close()
        print("Connection closed.", file=sys.stderr)

    except:
        # CTRL+C pressed or something bad
        print("\n *** Oh noes... ***")
        break

print("Shutting down...", file=sys.stderr)
server.close()
print("Goodbye.", file=sys.stderr)
# Stop listening
server.close()
