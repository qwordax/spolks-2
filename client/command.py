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

    sock.recv(BUFSIZE).decode('ascii')

    print('upload: started')

    with open(file_name, mode='rb') as file:
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

            if i % 512 == 0:
                print(
                    f'upload: {int(100 * (size+oob_size) / file_size):3d} %'
                    )

            i += 1

        print('upload: 100 %')
        print(f'upload: transmitted {size:,.0f} + {oob_size:,.0f} bytes')
        print('upload: ended')

def client_download(sock, args):
    if len(args) != 2:
        print('usage: download <file>')
        return

    sock.send(' '.join(args).encode('ascii'))
    response = sock.recv(BUFSIZE).decode('ascii')

    if response == 'not exists':
        print(f'error: \'{args[1]}\' does not exists')
        return

    file_info = sock.recv(BUFSIZE).decode('ascii').split()

    file_name = file_info[0]
    file_size = int(file_info[1])

    sock.send('ok'.encode('ascii'))

    print('download: started')

    with open(file_name, 'wb') as file:
        i = 0
        oob = file_size // 1024 // 4

        size = 0
        oob_size = 0

        while (size + oob_size) < file_size:
            if i < oob:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
                oob_size += file.write(sock.recv(BUFSIZE))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 0)
            else:
                size += file.write(sock.recv(BUFSIZE))

            if i % 512 == 0:
                print(
                    f'download: {int(100 * (size+oob_size) / file_size):3d} %'
                    )

            i += 1

        print('download: 100 %')
        print(f'download: received {size:,.0f} + {oob_size:,.0f} bytes')
        print('download: ended')

def client_unknown(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')
