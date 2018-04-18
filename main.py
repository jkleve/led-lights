from argparse import ArgumentParser
import binascii
import socket
import sys
import threading
import traceback


def receive(socket):
    while True:
        chunk = socket.recv(2048)
        print('Received: {chunk}'.format(**locals()))


def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (args.ip, 14077)

    try:
        sock.connect(server_address)
    except socket.error as e:
        print(e)
        # print(dir(e))
        # print(traceback.print_tb(e.__traceback__))
        # logging.exception(e)
        sys.exit(1)

    print('Connected')

    thread_recv = threading.Thread(name='recv', target=receive, args=(sock,))
    thread_recv.start()

    data = '31 ff 00 00 00 00 0f 3f'.replace(' ', '')
    data_binary = binascii.unhexlify(data)
    sock.sendall(data_binary)

    print('Data sent')


def cli():
    parser = ArgumentParser()
    parser.add_argument(type=str, default='10.0.0.89')
    args = parser.parse_args()
    return main(args)


if __name__ == '__main__':
    sys.exit(cli())
