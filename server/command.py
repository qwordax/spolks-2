import logging
import time

def command_echo(args):
    logging.info(' '.join(args))
    return '\n'.join(args[1:]) + '\n'

def command_time(args):
    logging.info(' '.join(args))

    if len(args) != 1:
        response = 'usage: time\n'
    else:
        response = time.ctime() + '\n'

    return response

def command_upload(args):
    logging.info(' '.join(args))

    if len(args) != 2:
        response = 'usage: upload <file>\n'
    else:
        response = '\n'

    return response

def command_download(args):
    logging.info(' '.join(args))

    if len(args) != 2:
        response = 'usage: download <file>\n'
    else:
        response = '\n'

    return response

def command_unknown(args):
    logging.error(f'unknown command \'{" ".join(args)}\'')
    return f'error: unknown command \'{" ".join(args)}\'\n'