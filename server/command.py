import logging
import os
import socket
import time

BUFSIZE = 1024

def server_echo(conn, args):
    response = '\n'.join(args[1:]) + '\n'
    conn.send(response.encode('ascii'))

def server_time(conn):
    response = time.ctime() + '\n'
    conn.send(response.encode('ascii'))

def server_upload(conn):
    file_info = conn.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    current_size = 0

    conn.send(str(current_size).encode('ascii'))

    logging.info('uploading . . .')

    with open(file_name, 'wb') as file:
        file.seek(current_size)

        i = 0
        oob = file_size // 1024 // 4

        size = current_size
        oob_size = 0

        while (size + oob_size) < file_size:
            if i < oob:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(conn.recv(BUFSIZE))
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(conn.recv(BUFSIZE))

            if i % 512 == 0:
                logging.info(
                    f'{int(100 * (size+oob_size) / file_size):3d} %'
                    )

            i += 1

        logging.info('100 %')
        logging.info(f'received {size:,.0f} + {oob_size:,.0f} bytes')
        logging.info(f'uploaded \'{file_name}\'')

def server_download(conn, args):
    if not os.path.exists(args[1]):
        conn.send('not exists'.encode('ascii'))
        return

    conn.send('exists'.encode('ascii'))

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    file_info = file_name + ' ' + str(file_size)
    conn.send(file_info.encode('ascii'))

    current_size = int(conn.recv(BUFSIZE).decode('ascii'))

    logging.info('downloading . . .')

    with open(file_name, mode='rb') as file:
        file.seek(current_size)

        i = 0
        oob = file_size // 1024 // 4

        size = current_size
        oob_size = 0

        for data in iter(lambda: file.read(BUFSIZE), b''):
            if i < oob:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                conn.send(data)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                conn.send(data)
                size += len(data)

            if i % 512 == 0:
                logging.info(
                    f'{int(100 * (size+oob_size) / file_size):3d} %'
                    )

            i += 1

        logging.info('100 %')
        logging.info(f'transmitted {size:,.0f} + {oob_size:,.0f} bytes')
        logging.info(f'downloaded \'{file_name}\'')

def server_unknown(conn, args):
    logging.error(f'unknown command \'{" ".join(args)}\'')

    response = f'error: unknown command \'{" ".join(args)}\'\n'
    conn.send(response.encode('ascii'))
