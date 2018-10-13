#!/usr/bin/env python

import os
import socket
import sys
<<<<<<< HEAD
=======
import binascii
import time
>>>>>>> 8ac8f4aadaac7513d833e8dad505d70a826cb697


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def jpsend(a='00', b='00', c='00'):
    print(type(a), a)
    # msg = bytes(3) # + bytearray.fromhex(b) + bytearray.fromhex(c)
    # msg=int_to_bytes(a)
<<<<<<< HEAD
    offset = bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')
    msg = offset + bytearray.fromhex(a) +bytearray.fromhex(b) + bytearray.fromhex(c)
    print(msg)
=======
    msg = bytearray.fromhex(a) +bytearray.fromhex(b) + bytearray.fromhex(c)
    print(msg)
    # msg[0] = a.to_bytes(1)
    # print(msg[0])
    # msg[1] = b;
    # msg[2] = c;
    # print(msg)
    # print(sys.stderr, 'sending "%s"' % msg)
>>>>>>> 8ac8f4aadaac7513d833e8dad505d70a826cb697
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
<<<<<<< HEAD
    # message = bytearray.fromhex('e0')
    # sock.sendall(message)
    command = input("JP2$ ")

=======
    message = bytearray.fromhex('e0')
    sock.sendall(message)
    command = input("JP2$ ")


>>>>>>> 8ac8f4aadaac7513d833e8dad505d70a826cb697
    if command == "quit" or command == "exit" or command == "q":
        break
    elif command == "help":
        continue
    elif command == "stopm":
        try:
<<<<<<< HEAD
            jpsend('06','00','00')
=======
            jpsend('f3')
            # msg = bytearray.fromhex('0E')
            # sock.sendall(msg)
>>>>>>> 8ac8f4aadaac7513d833e8dad505d70a826cb697
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


