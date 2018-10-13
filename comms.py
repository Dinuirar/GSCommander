#!/usr/bin/env python

import os
import socket
import sys
import binascii


def jpsend(a=0x00, b=0x00, c=0x00):
    print(type(a), a)
    msg = bytes(3) # + bytearray.fromhex(b) + bytearray.fromhex(c)
    msg=b'\x09\x00\x21'
    print(msg)
    a = 88
    # msg[0] = a.to_bytes(1)
    # print(msg[0])
    # msg[1] = b;
    # msg[2] = c;
    # print(msg)
    # print(sys.stderr, 'sending "%s"' % msg)
    sock.sendall(msg)


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("172.16.18.121", 43)
print(sys.stderr, 'connecting to %s port %s' % server_address)

try:
    sock.connect(server_address)
except:
    print("could not connect to the OBC")

command = ""

while command != "quit":
    # message = bytearray.fromhex('0E')
    # sock.sendall(message)
    # command = input("JP2$ ")
    command = "stopm"
    if command == "quit" or command == "exit" or command == "q":
        break
    elif command == "help":

        continue
    elif command == "stopm":
        try:
            jpsend(0xf3)
            print("stop motor")
        except:
            print("could not send message")
        continue
    elif command == "clear":

        continue
    elif command == "coefficients":
        continue




# print(sys.stderr, 'closing socket')
# sock.close()


