#!/usr/bin/env python
# coding: utf8

from __future__ import print_function, unicode_literals

import errno
import logging
import os
import os.path
import signal
import sys
import time

import crawlers
import utils


class _Daemon(object):
    def __init__(self, action):
        proxy6_dir = os.path.join(os.path.expanduser("~"), '.proxy6')
        self._action = action
        self._pid_file = os.path.join(proxy6_dir, '{}.pid'.format(action))
        self._log_file = os.path.join(proxy6_dir, '{}.log'.format(action))

    def _ensure_path(self):
        utils.path.ensure_path(os.path.dirname(self._pid_file))

    def _write_pid_file(self, pid):
        import fcntl
        import stat

        try:
            fd = os.open(self._pid_file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
        except OSError as e:
            logging.error(e, exc_info=True)
            return -1
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        assert flags != -1
        flags |= fcntl.FD_CLOEXEC
        r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
        assert r != -1
        try:
            fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
        except IOError:
            r = os.read(fd, 32)
            if r:
                logging.error('proxy6 {} already started at pid {}'.format(self._action, r))
            else:
                logging.error('proxy6 {} already started'.format(self._action))
            os.close(fd)
            return -1
        os.ftruncate(fd, 0)
        os.write(fd, str(pid))
        return 0

    def _freopen(self, mode, stream):
        oldf = open(self._log_file, mode)
        oldfd = oldf.fileno()
        newfd = stream.fileno()
        os.close(newfd)
        os.dup2(oldfd, newfd)

    def start(self):
        self._ensure_path()

        def handle_exit(signum, _):
            if signum == signal.SIGTERM:
                sys.exit(0)
            sys.exit(1)

        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)

        pid = os.fork()
        assert pid != -1

        if pid > 0:
            time.sleep(5)
            sys.exit(0)

        ppid = os.getppid()
        pid = os.getpid()

        if self._write_pid_file(pid) != 0:
            os.kill(ppid, signal.SIGINT)
            sys.exit(1)

        os.setsid()
        signal.signal(signal.SIG_IGN, signal.SIGHUP)

        print('proxy6 {} started'.format(self._action))
        os.kill(ppid, signal.SIGTERM)

        sys.stdin.close()
        try:
            self._freopen('a', sys.stdout)
            self._freopen('a', sys.stderr)
        except IOError as e:
            logging.error(e, exc_info=True)
            sys.exit(1)

    def stop(self):
        if not os.path.exists(self._pid_file):
            return logging.error('proxy6 {} not running'.format(self._action))
        with open(self._pid_file) as fp:
            pid = fp.read()
        if not pid or not pid.isdigit():
            return logging.error('{} not running'.format(self._action))

        pid = int(pid)
        if pid <= 0:
            return logging.error('pid is not positive: %d', pid)
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                logging.error('{} not running'.format(self._action))
                # always exit 0 if we are sure daemon is not running
                return
            sys.exit(1)

        # sleep for maximum 5s
        for _ in range(0, 100):
            try:
                # query for the pid
                os.kill(pid, 0)
            except OSError as e:
                if e.errno == errno.ESRCH:
                    break
            time.sleep(0.05)
        else:
            logging.error('timed out when stopping pid %d', pid)
            sys.exit(1)
        print('proxy6 {} stopped'.format(self._action))
        os.unlink(self._pid_file)


class _Commander(object):
    ACTION_START_FUNC = {
        'fetch': crawlers.fetch,
        'check': crawlers.check,
        'server': lambda *args, **kwargs: None,
    }

    def __getattr__(self, action):
        assert action in self.ACTION_START_FUNC
        self._action = action
        self._daemon = _Daemon(action)
        return self

    def __call__(self, command, config):
        assert command in {'start', 'stop', 'restart'}
        if command == 'stop':
            return self._daemon.stop()
        if command == 'restart':
            self._daemon.stop()

        if config.daemon:
            self._daemon.start()
        try:
            self.ACTION_START_FUNC[self._action](config)
        except KeyboardInterrupt:
            print('\rexiting, bye~')


commander = _Commander()
