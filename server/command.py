import logging
import time

def server_echo(args):
    return '\n'.join(args[1:]) + '\n'

def server_time(args):
    if len(args) != 1:
        response = 'usage: time\n'
    else:
        response = time.ctime() + '\n'

    return response

def server_upload(args):
    if len(args) != 2:
        response = 'usage: upload <file>\n'
    else:
        response = '\n'

    return response

def server_download(args):
    if len(args) != 2:
        response = 'usage: download <file>\n'
    else:
        response = '\n'

    return response

def server_unknown(args):
    logging.error(f'unknown command \'{" ".join(args)}\'')
    return f'error: unknown command \'{" ".join(args)}\'\n'
