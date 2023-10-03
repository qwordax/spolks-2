import socket
import sys

import command

def main():
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} <address> <port>')
        return

    address = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((address, port))

    while True:
        args = input('> ').split()

        if args == []:
            continue

        if args[0] == 'close' or args[0] == 'exit' or args[0] == 'quit':
            sock.send(' '.join(args).encode('ascii'))
            break

        if args[0] == 'echo':
            command.client_echo(sock, args)
        elif args[0] == 'time':
            command.client_time(sock, args)
        elif args[0] == 'upload':
            command.client_upload(sock, args)
        elif args[0] == 'download':
            command.client_download(sock, args)
        else:
            command.client_unknown(sock, args)

    sock.close()

if __name__ == "__main__":
    main()
