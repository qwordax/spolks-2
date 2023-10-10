import os
import socket

BUFSIZE = 1024
OOBSIZE = 4

def client_echo(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')

def client_time(sock, args):
    if len(args) != 1:
        print('usage: time')
        return

    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')

def client_upload(sock, args):
    if len(args) != 2:
        print('usage: upload <file>')
        return

    if not os.path.exists(args[1]):
        print(f'error: \'{args[1]}\' does not exists')
        return

    sock.send(' '.join(args).encode('ascii'))

    file_name = args[1]
    file_size = os.path.getsize(args[1])

    file_info = file_name + ' ' + str(file_size)
    sock.send(file_info.encode('ascii', errors='ignore'))

    print('upload: started')

    file = open(file_name, mode='rb')

    try:
        i = 0
        size = 0
        oob_size = 0

        for data in iter(lambda: file.read(BUFSIZE), b''):
            if i < OOBSIZE:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                sock.send(data)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                sock.send(data)
                size += len(data)

            i += 1

        print(f'upload: transmitted {oob_size:,.0f} urgent bytes')
        print(f'upload: transmitted {size:,.0f} bytes')

        print('upload: ended')
    finally:
        file.close()

def client_download(sock, args):
    if len(args) != 2:
        print('usage: download <file>')
        return

    sock.send(' '.join(args).encode())
    response = sock.recv(BUFSIZE).decode()

    if response == 'not exists':
        print(f'error: \'{args[1]}\' does not exists')
        return

    file_info = sock.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    if response == 'continue':
        file = open(file_name, 'ab')

        current_size = os.path.getsize(file_name)
        sock.send(str(current_size).encode('ascii'))

        print('download: continued')
    else:
        file = open(file_name, 'wb')

        current_size = 0

        print('download: started')

    try:
        i = 0
        size = 0
        oob_size = 0

        while (current_size + size + oob_size) < file_size:
            if i < OOBSIZE:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(sock.recv(BUFSIZE))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(sock.recv(BUFSIZE))

            i += 1

        print(f'download: received {oob_size:,.0f} urgent bytes')
        print(f'download: received {size:,.0f} bytes')

        print('download: ended')
    finally:
        file.close()

def client_unknown(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')
