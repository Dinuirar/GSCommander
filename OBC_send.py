#!/usr/bin/env python
import socket
import sys


def main():
    ip = "127.0.0.1"
    port = 12000

    try:

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.send(msg.encode("utf-8"))
        while True:
            data = input("Waiting for message to send: ")
            server_sock.sendto(data.encode("utf-8"), (ip, port))

    except KeyboardInterrupt:
        print("exiting")

    except OSError as err:
        print("OS error: {0}".format(err))

    except ValueError:
        print("Could not convert data to an integer.")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    finally:
        # server_sock.shutdown(socket.SHUT_RDWR)
        print("Closing socket...")
        server_sock.close()


if __name__ == "__main__":
    main()