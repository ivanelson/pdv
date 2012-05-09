#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
   Ivanelson Nunes
"""

import sys
import os

def regLog(strLog):
    import time
    data = time.localtime()
    #dataFormat = str(data[0]) + str(data[1]) + str(data[2])
    #dataFormat += ' ' + str(data[3]) + ':' + str(data[4])
    f=str(data[0]) + str(data[1]).zfill(2) + str(data[2]).zfill(2) + '.' + str(data[3]).zfill(2) + str(data[4]).zfill(2) + str(data[6]).zfill(2)
    LOG = open('/var/tmp/pyecf.pid', 'w')
    #LOG.write( dataFormat + ' = ' + cliche + '\n')
    LOG.write('%s - %s' % (f, strLog.strip()) + '\n')
    LOG.close()

try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except:
    MAXFD = 256

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null',
              newhome='/usr/local/lib', closeall=1):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("o primeiro fork falhou: (%d) %s\n" %
                         (e.errno, e.errstr))
        sys.exit(1)

    os.setsid()
    os.chdir(newhome)
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("o segundo fork falhou: (%d), %s\n" %
                         (e.errno, e.errstr))
        sys.exit(1)

    regLog('started with pid: %s' % os.getpid())

    fin = open(stdin, 'r')
    fout = open(stdout, 'a+')
    ferr = open(stderr, 'a+', 0)
    os.dup2(fin.fileno(), sys.stdin.fileno())
    os.dup2(fout.fileno(), sys.stdout.fileno())
    os.dup2(ferr.fileno(), sys.stderr.fileno())

    if closeall:
        for i in range(3, MAXFD):
            try:
                os.close(i)
            except:
                pass

def test():
    import time
    daemonize()
    while 1:
        time.sleep(10)

if __name__ == '__main__':
    test()
