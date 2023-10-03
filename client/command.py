import os

BUFSIZE = 256

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

    sock.send(file_name.encode('ascii'))
    sock.send(str(file_size).encode('ascii'))

    with open(file_name, mode='rb') as file:
        for data in iter(lambda: file.read(BUFSIZE), b''):
            sock.send(data)

def client_download(sock, args):
    if len(args) != 2:
        print('usage: download <file>')
        return

    sock.send(' '.join(args).encode('ascii'))
    response = sock.recv(BUFSIZE).decode('ascii')

    if response == 'not exists':
        print(f'error: \'{args[1]}\' does not exists')
        return

    file_name = sock.recv(BUFSIZE).decode('ascii')
    file_size = int(sock.recv(BUFSIZE).decode('ascii'))

    with open(file_name, 'wb') as file:
        size = 0

        while size < file_size:
            size += file.write(sock.recv(BUFSIZE))

def client_unknown(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(BUFSIZE).decode('ascii'), end='')
