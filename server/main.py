import logging
import socket
import sys

import command

BUFSIZ = 1024

def main():
    if len(sys.argv) != 3:
        print('usage: {0} <address> <port>'.format(sys.argv[0]))
        return

    address = sys.argv[1]
    port = int(sys.argv[2])

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-5s : %(message)s'
        )

    sock = socket.socket()

    sock.bind((address, port))

    sock.listen(1)

    working = True

    while working:
        logging.info('accepting . . .')

        conn, address = sock.accept()
        logging.info(f'accepted {address[0] + ":" + str(address[1])}')

        while True:
            args = conn.recv(BUFSIZ).decode('ascii').split()

            if args[0] == 'close':
                working = False
                break

            if args[0] == 'exit' or args[0] == 'quit':
                break

            logging.info(' '.join(args))

            if args[0] == 'echo':
                response = command.server_echo(args)
            elif args[0] == 'time':
                response = command.server_time(args)
            elif args[0] == 'upload':
                response = command.server_upload(args)
            elif args[0] == 'download':
                response = command.server_download(args)
            else:
                response = command.server_unknown(args)

            conn.send(response.encode('ascii'))

        logging.info(f'closed {address[0] + ":" + str(address[1])}')
        conn.close()

    logging.info('closing . . .')
    sock.close()

if __name__ == "__main__":
    main()
