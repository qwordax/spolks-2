import logging
import socket
import sys
import time

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
            command = conn.recv(BUFSIZ).decode('ascii')
            args = command.strip().split()

            if args[0] == 'close':
                working = False
                break

            if args[0] == 'exit' or args[0] == 'quit':
                break

            if args[0] == 'echo':
                logging.info(' '.join(args))
                response = '\n'.join(args[1:]) + '\n'
            elif args[0] == 'time':
                logging.info(' '.join(args))

                if len(args) > 1:
                    response = 'usage: time\n'
                else:
                    response = time.ctime() + '\n'
            else:
                logging.error(f'unknown command \'{" ".join(args)}\'')
                response = f'error: unknown command \'{" ".join(args)}\'\n'

            conn.send(response.encode('ascii'))

        logging.info(f'closed {address[0] + ":" + str(address[1])}')
        conn.close()

    logging.info('closing . . .')
    sock.close()

if __name__ == "__main__":
    main()
