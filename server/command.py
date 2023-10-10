import logging
import os
import socket
import time

BUFSIZE = 1024
OOBSIZE = 4

last_address = None
last_file_name = None

fatal = False

def server_echo(conn, args):
    response = '\n'.join(args[1:]) + '\n'
    conn.send(response.encode('ascii'))

def server_time(conn, args):
    response = time.ctime() + '\n'
    conn.send(response.encode('ascii'))

def server_upload(conn, args):
    file_info = conn.recv(BUFSIZE).decode('ascii', errors='ignore').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    logging.info('uploading . . .')

    file = open(file_name, 'wb')

    try:
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

        logging.info(f'received {oob_size:,.0f} urgent bytes')
        logging.info(f'received {size:,.0f} bytes')

        logging.info(f'uploaded \'{file_name}\'')
    finally:
        file.close()

def server_download(conn, address, args):
    global last_address
    global last_file_name
    global fatal

    if not os.path.exists(args[1]):
        conn.send('not exists'.encode('ascii'))
        return

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    if (last_address is not None and
        last_address == address and
        last_file_name == file_name and
        fatal is True):
        conn.send('continue'.encode('ascii'))

        file_info = file_name + ' ' + str(file_size)
        conn.send(file_info.encode())

        logging.info('continue downloading . . .')

        file = open(file_name, mode='rb')

        current_size = int(conn.recv(BUFSIZE).decode('ascii'))
        file.seek(current_size)
    else:
        conn.send('exists'.encode('ascii'))

        file_info = file_name + ' ' + str(file_size)
        conn.send(file_info.encode('ascii'))

        logging.info('downloading . . .')

        file = open(file_name, mode='rb')

        current_size = 0

    fatal = False

    try:
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

        logging.info(f'transmitted {oob_size:,.0f} urgent bytes')
        logging.info(f'transmitted {size:,.0f} bytes')

        logging.info(f'downloaded \'{file_name}\'')
    except TimeoutError:
        last_address = address
        last_file_name = file_name

        logging.error(f'timed out')
    finally:
        file.close()

def server_unknown(conn, args):
    logging.error(f'unknown command \'{" ".join(args)}\'')

    response = f'error: unknown command \'{" ".join(args)}\'\n'
    conn.send(response.encode('ascii'))
