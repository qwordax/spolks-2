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
        format='%(levelname)-8s : %(message)s'
        )

    socket.setdefaulttimeout(30)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))

    sock.listen(1)

    working = True
    timeout = 0

    while working and timeout < 3:
        logging.info('accepting . . .')

        try:
            conn, address = sock.accept()
            logging.info(f'accepted {address[0] + ":" + str(address[1])}')
        except TimeoutError:
            logging.info('timeout'); timeout += 1
            continue

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
                    command.server_time(conn)
                elif args[0] == 'upload':
                    command.server_upload(conn, address)
                elif args[0] == 'download':
                    command.server_download(conn, address, args)
                else:
                    command.server_unknown(conn, args)
        except ConnectionAbortedError:
            command.FATAL = True

            logging.critical(
                f'connection aborted {address[0]+":"+str(address[1])}')
        except ConnectionResetError:
            command.FATAL = True

            logging.critical(
                f'connection reset {address[0]+":"+str(address[1])}')
        except TimeoutError:
            command.FATAL = True

            logging.critical(
                f'timeout {address[0]+":"+str(address[1])}')
        finally:
            logging.info(
                f'closed {address[0]+":"+str(address[1])}')

            conn.close()

    logging.info('closing . . .')
    sock.close()

if __name__ == "__main__":
    main()
