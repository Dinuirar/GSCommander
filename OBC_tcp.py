#!/usr/bin/env python
import socket
import sys
import traceback


def main():
    try:
        server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_sock.bind(("127.0.0.1", 12000))
        server_sock.listen(1)
        print("Waiting for connection...")
        conn, address = server_sock.accept()
        print("Waiting for message...")
        while True:
            data = conn.recv(1024)
            if not data:
                print("Connection closed")
                break
            msg = data.decode("utf-8")
            print("Message: " + msg)
            conn.send(bytes("received message: "+msg, "utf-8"))

    except KeyboardInterrupt:
        print("exiting")

    except OSError:  # as err:
        # print("OS error: {0}".format(err))
        # extype, value, tb = sys.exc_info()
        traceback.print_exc()
        # pdb.post_mortem(tb)

    except ValueError:
        print("Could not convert data to an integer.")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    finally:
        #server_sock.shutdown(socket.SHUT_RDWR)
        print("Closing socket...")
        server_sock.close()

        
if __name__ == "__main__":
    main()
