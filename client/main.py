import socket
import sys

BUFSIZ = 1024

def main():
    if len(sys.argv) != 3:
        print('usage: {0} <address> <port>'.format(sys.argv[0]))
        return

    address = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket()

    sock.connect((address, port))

    while True:
        args = input('> ').split()

        if args == []:
            continue

        sock.send(' '.join(args).encode('ascii'))

        if args[0] == 'close' or args[0] == 'exit' or args[0] == 'quit':
            break

        print(sock.recv(BUFSIZ).decode('ascii'), end='')

    sock.close()

if __name__ == "__main__":
    main()
