#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import decf
import base
import os 
from subprocess import *


if __name__ == '__main__':
    #MY_HOME = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0].strip()
    #print MY_HOME 
    decf.daemonize()

    base.logDebug('INSTANCIANDO CLASS BASE ECF')

    ecf = base.Base()
    call("echo 'fin_wait' > /u1/caixa/dev/tty1/DECF.cfg",shell=True)
    fileIn = '/u1/caixa/dev/tty1/pergunta'
    fileOut = '/u1/caixa/dev/tty1/resposta'

    while 1:
        #print 'running!!!!'
        #f.write(time.asctime() + '\n')
        #f.flush()
        WAIT = base.readAsk('/u1/caixa/dev/tty1/DECF.cfg')
        if WAIT.strip() == 'wait':
            base.logDebug(WAIT.strip())
            ecf.doCmd(fileIn, fileOut)
            retShell=call("echo 'fin_wait' > /u1/caixa/dev/tty1/DECF.cfg",shell=True)
            if retShell <> 0: call("echo 'fin_wait' > /u1/caixa/dev/tty1/DECF.cfg",shell=True)
        time.sleep(0.050)
