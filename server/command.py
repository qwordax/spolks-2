import logging
import os
import socket
import time

BUFSIZE = 1024
OOBSIZE = 4

def server_echo(conn, args):
    response = '\n'.join(args[1:]) + '\n'
    conn.send(response.encode('ascii'))

def server_time(conn, args):
    response = time.ctime() + '\n'
    conn.send(response.encode('ascii'))

def server_upload(conn, args):
    file_info = conn.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    logging.info('uploading . . .')

    with open(file_name, 'wb') as file:
        i = 0
        size = 0
        oob_size = 0

        while (size + oob_size) < file_size:
            if i < OOBSIZE:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(conn.recv(BUFSIZE))
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(conn.recv(BUFSIZE))

            i += 1

    logging.info(f'received {size} bytes')
    logging.info(f'received {oob_size} urgent bytes')

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

    logging.info('downloading . . .')

    with open(file_name, mode='rb') as file:
        i = 0
        size = 0
        oob_size = 0

        for data in iter(lambda: file.read(BUFSIZE), b''):
            if i < OOBSIZE:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                conn.send(data)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                conn.send(data)
                size += len(data)

            i += 1

    logging.info(f'transmitted {size} bytes')
    logging.info(f'transmitted {oob_size} urgent bytes')

    logging.info(f'downloaded \'{file_name}\'')

def server_unknown(conn, args):
    logging.error(f'unknown command \'{" ".join(args)}\'')

    response = f'error: unknown command \'{" ".join(args)}\'\n'
    conn.send(response.encode('ascii'))
