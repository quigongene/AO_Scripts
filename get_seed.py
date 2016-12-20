#!/usr/bin/python3
# Get AO seed from server

import socket  # for sockets
import sys  # for exit

# create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

host = "37.18.192.41"
port = 7105

try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    # could not resolve
    print("Hostname could not be resolved. Exiting")
    sys.exit()

# Connect to remote server
s.connect((remote_ip, port))

# Now receive data
reply = s.recv(1024)

reply = (reply[6:])

reply = reply.decode('utf-8')

print(reply)
