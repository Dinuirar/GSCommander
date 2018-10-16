#!/usr/bin/env python

import os
import socket
import sys


# def int_to_bytes(x):
#     return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def jpsend(a='00', b='00', c='00'):
    # print(type(a), a)
    # print(type(b), b)
    # print(type(c), c)
    offset = bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')+bytearray.fromhex('00')
    msg = offset + bytearray.fromhex(a) +bytearray.fromhex(b) + bytearray.fromhex(c)
    print(msg)
    sock.sendall(msg)


def printhelp():
    help = open('help.info','r')
    msgg = help.read()
    print(msgg)
    help.close()


def connect():
    try:
        sock.connect(server_address)
        print('connected to %s port %s' % server_address)
    except:
        print("could not connect to the OBC")


os.system('CLS')
print("Welcome to BEXUS LUSTRO ground station, fasten your seatbelts and have fun\r\n")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("172.16.18.121", 43)
# print(sys.stderr, 'connecting to %s port %s' % server_address)
print('connecting to %s port %s' % server_address)

connect()

command = ""
sendfail = "could not send command"
badarg = "invalid arguments. write \"help\" to see helpfile"
badinput = "too many arguments passed. write \"help\" to see helpfile"
args_ok = 0

while command != "quit":
    # message = bytearray.fromhex('e0')
    # sock.sendall(message)

    input_data = input("JP2$ ").split()
    command = input_data[0]
    if input_data.__len__() > 3:
        print(badinput)

    if command == "quit" or command == "exit" or command == "q":
        break
    elif command == "help":
        printhelp()
        continue
    elif command == "reset":        # reset the OBC
        try:
            jpsend('06')
            print("reset the OBC")
        except:
            print(sendfail)
        continue
    elif command == "stopm" or command == "stop" or command == "s":        # stop motor
        try:
            jpsend('03')
            print("stop motor")
        except:
            print(sendfail)
        continue
    elif command == "startm" or command == "start":       # start motor with default rotation rate
        try:
            jpsend('0c')
            print("start motor")
        except:
            print(sendfail)
        continue
    elif command == "enstream" or command == "en":     # enable downstream
        try:
            jpsend('11')
            print("enable downstream")
        except:
            print(sendfail)
        continue
    elif command == "disstream" or command == "dis":    # disable downstream
        try:
            jpsend('12')
            print("disable downstream")
        except:
            print(sendfail)
        continue
    elif command == "setspeed" or command == "ss":        # set motor speed in % 
        try:
            # arg1 = input_data[1]  ## if direction needed
            # if arg1 == 'f':
            #     arg1 = '01'
            # elif arg1 == 'b':
            #     arg1 = '02'
            # else:
            #     raise Exception

            arg1 = int(input_data[1])
            if arg1 < 0 or arg1 > 100:
                raise Exception
            print(arg1, "\t", arg1)
            arg1 = str(hex(arg1).split('x')[-1])
            args_ok = 1
        except:
            print(badarg)

        if args_ok == 1:
            try:
                jpsend('01',arg1)
                print("motor speed set to: ", arg1)
            except:
                print(sendfail)
            args_ok = 0
            continue
    elif command == "disconnect" or command == "disc":    # disconnects from server
        try:
            sock.close()
            print('disconnected from %s port %s' % server_address)
        except:
            print(sendfail)
        continue
    elif command == "connect" or command == "con":    # disconnects from server
        try:
            connect()
        except:
            print(sendfail)
        continue
    elif command == "check" or command == "ch":    # disconnects from server
        try:
            jpsend()
        except:
            print(sendfail)
        continue

# print(sys.stderr, 'closing socket')
# sock.close()


