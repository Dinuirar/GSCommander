#!/usr/bin/env python
import socket
import os
import sys
import logging
from logmod import *


def send(self, msg):
    if len(msg) % 2:
        msg = "0" + msg  # add zero to hex if length of string is odd
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, int(self.port)))
        sock.settimeout(self.TIMEOUT)
        sock.send(msg.encode("utf-8"))
    except socket.timeout:
        msg = "Socket timeout. Data not received"
        log_error(msg)
    except OSError:
        msg = "OS error. Trace in log."
        log_exception(msg)
    except KeyboardInterrupt:
        log_info("Method manually interrupted. Back to main loop")
    else:
        sock.close()


def streamDown(self):
    # TODO: keyboardinterrupt does not work on windows?
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip, int(self.port)))
        log_info("Waiting for data...")
        if os.path.exists(self.results_file):
            # aw = 'a'
            aw = 'ab'  # open in binary mode
        else:
            # aw = 'w'
            aw = 'wb'  # open in binary mode
        try:
            f = open(self.results_file, aw)
            while True:
                # if timeout show message and continue, else save data to file
                try:
                    # sock.setblocking(False)
                    sock.settimeout(self.TIMEOUT)

                except socket.timeout:
                    msg = "Socket timeout. Data not received"
                    log_error(msg)
                except (KeyboardInterrupt, SystemExit):
                    log_info("Method manually interrupted. Back to main loop")
                else:
                    data, address = sock.recvfrom(self.BUFFER_SIZE)
                    # f.write(data.decode("utf-8"))
                    f.write(data)  # save to file in binary mode
                    print(data)
        except OSError:
            msg = "OS error. Trace in log."
            log_exception(msg)

    except OSError:
        msg = "OS error. Trace in log."
        log_exception(msg)

    except ValueError:
        msg = "Could not convert data to an integer."
        log_exception(msg)

    except KeyboardInterrupt:
        log_info("Method manually interrupted. Back to main loop")

    except:
        msg = "Unexpected error:", sys.exc_info()[0]
        log_exception(msg)
        raise

    else:
        log_info("Closing connection...")
        # sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        f.close()
        return


def sendrec(self, msg):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, int(self.port)))
        sock.send(msg.encode("utf-8"))
        sock.settimeout(self.TIMEOUT)
        data = sock.recv(self.BUFFER_SIZE)
    except socket.timeout:
        log_warning("Socket timeout. Data not received")
        return None
    except socket.error:
        log_error("Could not connect to chosen address")
        return None
    else:
        sock.close()
        return data.decode("utf-8")


def save_results(self, data):
    if data is not None:
        if os.path.exists(self.results_file):
            aw = 'a'
            log_info("appending to file {0}".format(self.results_file))
        else:
            aw = 'w'
            log_info("file for result will be created")
        f = open(self.results_file, aw)
        f.write(data)
        f.close()
    else:
        log_info("Data = None - no data saved")