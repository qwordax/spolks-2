import socket

BUFSIZ = 1024

def main():
    address = input('address: ')
    port = int(input('port: '))

    print('. . .')

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
