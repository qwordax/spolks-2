import logging
import socket
import time

BUFSIZ = 1024

def main():
    address = input('address: ')
    port = int(input('port: '))

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-5s : %(message)s'
        )

    print('. . .')

    sock = socket.socket()

    sock.bind((address, port))

    sock.listen(1)

    working = True

    while working:
        conn, address = sock.accept()
        logging.info(f'accepted {address[0] + ":" + str(address[1])}')

        while True:
            command = conn.recv(BUFSIZ).decode('ascii')

            if command == 'close\n':
                working = False
                break

            if command == 'exit\n' or command == 'quit\n':
                break

            if command[:4] == 'echo':
                logging.info(command.strip())
                response = '\n'.join(command[5:].split()) + '\n'
            elif command[:5] == 'time\n':
                logging.info(command.strip())
                response = time.ctime() + '\n'
            else:
                logging.error(f'unknown command \'{command.strip()}\'')
                response = f'error: unknown command \'{command.strip()}\'\n'

            conn.send(response.encode('ascii'))

        logging.info(f'closed {address[0] + ":" + str(address[1])}')
        conn.close()

    sock.close()

if __name__ == "__main__":
    main()
