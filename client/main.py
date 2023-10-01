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
        command = ' '.join(input('> ').split()) + '\n'

        if command == '\n':
            continue

        sock.send(command.encode('ascii'))

        if command == 'close\n' or command == 'exit\n' or command == 'quit\n':
            break

        print(sock.recv(BUFSIZ).decode('ascii'), end='')

    sock.close()

if __name__ == "__main__":
    main()
