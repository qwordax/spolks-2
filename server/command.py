import logging
import time

BUFSIZE = 256

def server_echo(conn, args):
    response = '\n'.join(args[1:]) + '\n'
    conn.send(response.encode('ascii'))

def server_time(conn, args):
    response = time.ctime() + '\n'
    conn.send(response.encode('ascii'))

def server_upload(conn, args):
    file_name = conn.recv(BUFSIZE).decode('ascii')
    file_size = int(str(conn.recv(BUFSIZE).decode('ascii')))

    with open(file_name, 'wb') as file:
        size = 0

        while size < file_size:
            size += file.write(conn.recv(BUFSIZE))

def server_download(conn, args):
    pass

def server_unknown(conn, args):
    logging.error(f'unknown command \'{" ".join(args)}\'')

    response = f'error: unknown command \'{" ".join(args)}\'\n'
    conn.send(response.encode('ascii'))
