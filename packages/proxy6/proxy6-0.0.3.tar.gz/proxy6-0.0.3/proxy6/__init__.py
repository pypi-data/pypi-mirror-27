#!/usr/bin/env python
# coding: utf8

from __future__ import print_function, unicode_literals

import argparse
import logging
import logging.config
import os
import sys
from functools import wraps

import commander
import errors

__version__ = '0.0.3'
_usage = '''proxy6 fetch/check/server [start/stop/restart] [-c /config/file/path] [-d]

example: 
 - `proxy6 fetch -c /my/config/file.json`: start a proxy fetcher with specified config file.
 - `proxy6 fetch stop`: stop my proxy fetcher.
 - `proxy6 server restart -c /my/config/file.json -d`: start a proxy server with specified config file and run on daemon mode.

'''


def exception_handler(func):
    @wraps(func)
    def _deco(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.Proxy6Exception as err:
            sys.stderr.write('proxy6 exception: {}\n'.format(err.msg))

    return _deco


@exception_handler
def main():
    parser = argparse.ArgumentParser(prog='proxy6',
                                     usage=_usage,
                                     version=__version__,
                                     description='proxy6: A 2/3 compatible crawler http proxy pool.')
    parser.add_argument('-c', '--config', default=None, metavar='/config/file/path', help='server side config path')
    parser.add_argument('-d', '--daemon', default=False, help='daemon mode', action='store_true')

    args, actions = parser.parse_known_args()

    if not actions:
        return parser.print_help()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s')

    if actions[0] in {'fetch', 'server', 'check'}:
        if len(actions) < 2:
            actions.append('start')
        if actions[1] not in {'start', 'stop', 'restart'}:
            raise errors.CommandError(
                'command `proxy {} {}` not found, use `proxy6 -h` list all commands.'.format(*actions))
        if args.daemon and os.name != 'posix':
            raise errors.OSError('daemon mode is only supported on Unix like system.')
        getattr(commander.commander, actions[0])(actions[1], args)
    else:
        raise errors.CommandError('command `proxy {}` not found, use `proxy6 -h` list all commands.'.format(actions[0]))


if __name__ == '__main__':
    main()
