#!/usr/bin/python
import socket
import sys

# af_inet? sock_stream?
# Create a TCP/IP socket to listen on
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent "address already in use" on server restart
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind socket to port 8081 on all interfaces
# interfaces?
server_address = ("localhost", 8081)
print "starting up on %s port %s" % server_address
server.bind(server_address)

# Listen for connections
server.listen(5)

# Wait for one incoming connection
connection, client_address = server.accept()
print "connection from", connection.getpeername()

# Recieve something
data = connection.recv(4096)
if data:
    print "Received ", repr(data)

    # send it back all pretty
    data = data.rstrip()
    connection.send("%s\n%s\n%s\n" % ('-'*80, data.center(80), '-'*80))
    print "Response sent!"

# Close the connection on our side
connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
connection.close()
print "Connection close."

# Stop listening
server.close()
