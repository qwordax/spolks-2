def client_echo(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(256).decode('ascii'), end='')

def client_time(sock, args):
    if len(args) != 1:
        print('usage: time')
        return

    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(256).decode('ascii'), end='')

def client_upload(sock, args):
    pass

def client_download(sock, args):
    pass

def client_unknown(sock, args):
    sock.send(' '.join(args).encode('ascii'))
    print(sock.recv(256).decode('ascii'), end='')
