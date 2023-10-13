import logging
import os
import socket
import time

FATAL = False

last_address = None
last_file_name = None

BUFSIZE = 1024

def server_echo(conn, args):
    response = '\n'.join(args[1:]) + '\n'
    conn.send(response.encode('ascii'))

def server_time(conn):
    response = time.ctime() + '\n'
    conn.send(response.encode('ascii'))

def server_upload(conn, address):
    global FATAL

    global last_address
    global last_file_name

    file_info = conn.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    is_continue = (last_address is not None and
                   last_address == address[0] and
                   last_file_name == file_name and
                   FATAL is True)

    if is_continue:
        current_size = os.path.getsize(file_name)
        file_mode = 'ab'
    else:
        current_size = 0
        file_mode = 'wb'

    conn.send(str(current_size).encode('ascii'))

    logging.info('uploading . . .')

    FATAL = False

    last_address = address[0]
    last_file_name = file_name

    with open(file_name, file_mode) as file:
        i = 0
        oob = file_size // 1024 // 4

        size = 0
        oob_size = 0

        while (current_size + size + oob_size) < file_size:
            if i < oob:
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(conn.recv(BUFSIZE))
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(conn.recv(BUFSIZE))

            full_size = current_size+size+oob_size

            if i % 512 == 0:
                logging.info(f'{int(100*full_size/file_size):3d} %')

            i += 1

        logging.info('100 %')
        logging.info(f'received {size:,.0f} + {oob_size:,.0f} bytes')
        logging.info(f'uploaded \'{file_name}\'')

def server_download(conn, address, args):
    global FATAL

    global last_address
    global last_file_name

    if not os.path.exists(args[1]):
        conn.send('not exists'.encode('ascii'))
        return

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    is_continue = (last_address is not None and
                   last_address == address[0] and
                   last_file_name == file_name and
                   FATAL is True)

    if is_continue:
        conn.send('continue'.encode('ascii'))
    else:
        conn.send('exists'.encode('ascii'))

    file_info = file_name + ' ' + str(file_size)
    conn.send(file_info.encode('ascii'))

    current_size = int(conn.recv(BUFSIZE).decode('ascii'))

    logging.info('downloading . . .')

    FATAL = False

    last_address = address[0]
    last_file_name = file_name

    with open(file_name, mode='rb') as file:
        file.seek(current_size)

        i = 0
        oob = file_size // 1024 // 4

        size = 0
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

            full_size = current_size+size+oob_size

            if i % 512 == 0:
                logging.info(f'{int(100*full_size/file_size):3d} %')

            i += 1

        logging.info('100 %')
        logging.info(f'transmitted {size:,.0f} + {oob_size:,.0f} bytes')
        logging.info(f'downloaded \'{file_name}\'')

def server_unknown(conn, args):
    logging.error(f'unknown command \'{" ".join(args)}\'')

    response = f'error: unknown command \'{" ".join(args)}\'\n'
    conn.send(response.encode('ascii'))
