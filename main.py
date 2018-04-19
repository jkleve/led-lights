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


def server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip, port)
    print('bind')
    sock.bind(server_address)
    print('listen')
    sock.listen(1)
    print('accept')
    connection, address = sock.accept()
    print(dir(connection))
    print(connection)


def main(args):
    if args.type == 'server':
        server(args.host, args.port)
        return 0

    # server_thread = threading.Thread(name='server', target=server, args=(args.host, args.port))
    # server_thread.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (args.host, args.port)

    try:
        sock.connect(server_address)
    except socket.error as e:
        print(e)
        sys.exit(1)

    print('Connected')

    # thread_recv = threading.Thread(name='recv', target=receive, args=(sock,))
    # thread_recv.start()

    data = '31 ff 00 00 00 00 0f 3f'.replace(' ', '')
    data_binary = binascii.unhexlify(data)
    sock.sendall(data_binary)

    print('Data sent')


def cli():
    parser = ArgumentParser()
    parser.add_argument('host', type=str, nargs='?', default='localhost')
    parser.add_argument('-p', '--port', type=int, default=3642)
    parser.add_argument('--type', choices=('client', 'server'), default='client')
    args = parser.parse_args()
    return main(args)


if __name__ == '__main__':
    sys.exit(cli())
