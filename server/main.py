import logging
import socket
import sys

import command

def main():
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} <address> <port>')
        return

    address = sys.argv[1]
    port = int(sys.argv[2])

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-5s : %(message)s'
        )

    socket.setdefaulttimeout(30)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))

    sock.listen(1)

    working = True

    while working:
        logging.info('accepting . . .')

        conn, address = sock.accept()
        logging.info(f'accepted {address[0] + ":" + str(address[1])}')

        try:
            while True:
                args = conn.recv(command.BUFSIZE).decode('ascii').split()

                if args[0] == 'close':
                    working = False
                    break

                if args[0] == 'exit' or args[0] == 'quit':
                    break

                logging.info(' '.join(args))

                if args[0] == 'echo':
                    command.server_echo(conn, args)
                elif args[0] == 'time':
                    command.server_time(conn, args)
                elif args[0] == 'upload':
                    command.server_upload(conn, args)
                elif args[0] == 'download':
                    command.server_download(conn, args)
                else:
                    command.server_unknown(conn, args)
        except TimeoutError:
            logging.error(f'timed out {address[0] + ":" + str(address[1])}')
        finally:
            logging.info(f'closed {address[0] + ":" + str(address[1])}')
            conn.close()

    logging.info('closing . . .')
    sock.close()

if __name__ == "__main__":
    main()
