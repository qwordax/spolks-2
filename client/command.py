import os
import socket

BUFSIZE = 1024

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
    sock.send(file_info.encode('ascii'))

    current_size = int(sock.recv(BUFSIZE).decode('ascii'))

    with open(file_name, 'rb') as file:
        file.seek(current_size)

        i = 0
        oob = file_size // 1024 // 4

        size = 0
        oob_size = 0

        for data in iter(lambda: file.read(BUFSIZE), b''):
            if i < oob:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                sock.send(data)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)

                oob_size += len(data)
            else:
                sock.send(data)
                size += len(data)

            full_size = current_size+size+oob_size

            if i % 512 == 0:
                print(f'{int(100*full_size/file_size):3d} %')

            i += 1

        print('100 %')
        print(f'transmitted {size:,.0f} + {oob_size:,.0f} bytes')

def client_download(sock, args):
    if len(args) != 2:
        print('usage: download <file>')
        return

    sock.send(' '.join(args).encode('ascii'))
    response = sock.recv(BUFSIZE).decode('ascii')

    if response == 'not exists':
        print(f'error: \'{args[1]}\' does not exists')
        return

    is_continue = response == 'continue'

    file_info = sock.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    if is_continue:
        current_size = os.path.getsize(file_name)
        file_mode = 'ab'
    else:
        current_size = 0
        file_mode = 'wb'

    sock.send(str(current_size).encode('ascii'))

    with open(file_name, file_mode) as file:
        i = 0
        oob = file_size // 1024 // 4

        size = 0
        oob_size = 0

        while (current_size + size + oob_size) < file_size:
            if i < oob:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(sock.recv(BUFSIZE))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(sock.recv(BUFSIZE))

            full_size = current_size+size+oob_size

            if i % 512 == 0:
                print(f'{int(100*full_size/file_size):3d} %')

            i += 1

        print('100 %')
        print(f'received {size:,.0f} + {oob_size:,.0f} bytes')

def client_unknown(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')
