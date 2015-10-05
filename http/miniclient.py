#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8081))
message = "Hi, I'm connecting from Libby's mini-client!"
s.send(message)
print "Sent: %s" % message
data = s.recv(1024)
s.close() 
print "Recieved: "
print data
