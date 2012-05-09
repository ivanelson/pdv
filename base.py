#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Ivanelson Nunes'

import os, sys
import DarumaMethods
from inspect import getargspec
from ctypes import *

def readAsk(fileIn):
    cliche = ''
    try:
        fileIn = open(fileIn, 'r')
        inLines = fileIn.readlines()
        for line in inLines:
            cliche = line
    except IOError as e:
        print e
        sys.close(1)
    finally:
        fileIn.close()
    return cliche

def saveLog(strLog, fileName='ECF'):
    retFormat = 0
    if type(strLog) is tuple:
        aux = str(strLog[0]).zfill(4)
        retFormat = '%s%s' % (aux, "".join(strLog[1:]))
        #print 'Retorno => %s' % ([i for i in strLog])
    else:
        retFormat = str(strLog).zfill(4)
        #print 'Retorno => %s' % retFormat

    import time
    data = time.localtime()
    dataFormat = str(data[0]) + str(data[1]) + str(data[2])
    dataFormat += ' ' + str(data[3]) + ':' + str(data[4])
    LOG = open(fileName, 'w')
    #LOG.write( dataFormat + ' = ' + cliche + '\n')
    LOG.write(retFormat + '\n')
    LOG.close()

def logDebug(strLog):
##################################### Log provisorio ################################
    import time
    data = time.localtime()
    #dataFormat = str(data[0]) + str(data[1]) + str(data[2])
    #dataFormat += ' ' + str(data[3]) + ':' + str(data[4])
    f = str(data[0]) + str(data[1]).zfill(2) + str(data[2]).zfill(2) + '.' + str(data[3]).zfill(2) + str(data[4]).zfill(2) + str(data[6]).zfill(2)
    LOG = open('/var/tmp/pyecf.log.%s' % f[0:8], 'a')
    #LOG.write( dataFormat + ' = ' + cliche + '\n')
    LOG.write('%s - %s' % (f, strLog.strip()) + '\n')
    LOG.close()
#####################################      EndLog    ################################

class Base(object):
    """
    - Arquivo de tags: ./DarumaFramework/DarumaFramework.xml
    - rVerificarGTCodificado_ECF_Daruma(self, *args): A tag ECF\RetornarAvisoErro deve esta habilitada
    - rInfoEstendida_ECF_Daruma: A tag <ReceberInfoEstendida>1</ReceberInfoEstendida> deve esta habilitada
    - Estou usando controle de porta automatico: Darumaframework.xml
    - Libs auxiliares devem estar no mesmo path da minha aplicacao. Ex;liblebin.
    """
    def __init__(self):
        myLib = '%s/DarumaFramework/libDarumaFramework.so' % \
                os.path.split(os.path.abspath(os.path.realpath(__file__)))[0].strip() 
        #self.iDrv = cdll.LoadLibrary('./usr/lib/libDarumaFramework.so')
        self.iDrv = cdll.LoadLibrary(myLib) 
        try:
            pass 
        except OSError:
            logDebug('NO INITIALIZE: OSError! Lib not found') 
            print 'Library file not found! %s' % myLib 
            sys.close(1)
        except e:
            logDebug('NO INITIALIZE: %s - %s' % (e.errno, e.errstr) )
            print '%s - %s' % (e.errno, e.errstr) 
            sys.close(1)


        #if '/usr/lib' not in sys.path: sys.path.append('/usr/local/lib/liblebin.so')  
        #logDebug('sys.path: %s ' % sys.path) 

        
        self.Status = None
        self.COO    = ' '*6
        self.CCF    = ' '*6
        self.TOTAL  = ' '*12
        self.GT     = ' '*60
        self.SERIE  = ' '*60
        self.STATUSECF = ' '*14
        logDebug('LOAD INIT BASE')


    def doCmd(self, fileIn, fileOut): #iDrv, self.methods, auxArgs, self.listParams)

        listParams = readAsk(fileIn).split(chr(28))
        method     = listParams[0].strip()
        retCmd     = None
        #auxArgs    = getattr(Base, method)
        listParams = listParams[1:]

        numberOfParameters = 0
	print 'bening...'
        if method in dir (DarumaMethods):
            listParamsByReference = []
	    #numberOfParameters = len(eval('DarumaMethods.' + method))
	    numberOfParameters = len(getattr(DarumaMethods,method))
	    print numberOfParameters
            listTypes = []
            totalParameters = numberOfParameters + len(listParams)
            for i in xrange(totalParameters):
                listTypes.append(c_char_p)

            if numberOfParameters > 0:   # Parameters by reference
		print 'has parameters by reference...'
                for i in getattr(DarumaMethods, method):
                    pName, pLength = i
		    #pLength = pLength * "' '"
		    # create variable by reference
                    exec('%s = %s' % (pName, pLength * "' '") )
                    listParamsByReference.append( eval(pName) )

            allParams = listParams + listParamsByReference
	    print listTypes
            if listTypes:
		print 'registry of types ...'
                '%s.%s.argtypes = %s ' % (self.iDrv, method, listTypes)
            else:
                '%s.%s.argtypes = %s ' % (self.iDrv, method, None)

            '%s.%s.restype = %s ' % (self.iDrv, method, c_int )

            if allParams:
		print 'Running with parametrs...'
                #print ' %s.%s (*%s) ' % (self.iDrv, method,  allParams)
                retCmd = getattr(self.iDrv, method) (*allParams)
		print 'Retorno = %s' % retCmd 
            else:
                #retCmd = ' %s.%s () ' % (self.iDrv, method )
		print 'Running without parametrs...'
                #print ' %s.%s (*%s) ' % (self.iDrv, method,  allParams)
                retCmd = getattr(self.iDrv, method) ()
		print 'Retorno = %s' % retCmd 
	    print allParams

        """
        if hasattr(self.iDrv, method):
            if getargspec(auxArgs)[1] == None:
                logDebug('SEM PASSAGEM DE ARGUMENTOS')
                retCmd = getattr(Base, method) (self)
            else:
                logDebug('COM PASSAGEM DE ARGUMENTOS')
                retCmd = getattr(Base, method)(self,*listParams)
        else:
                #print "method doesn't exists"
                logDebug('method doesn''t exists')
                return
        """
        saveLog(retCmd,fileOut)

    def  iLeituraX_ECF_Daruma(self):
        self.iDrv.iLeituraX_ECF_Daruma.argtypes = 	None
        self.iDrv.iLeituraX_ECF_Daruma.restype = c_int
        self.Status = self.iDrv.iLeituraX_ECF_Daruma();
        return self.Status

    def iReducaoZ_ECF_Daruma(self, *args):
        self.iDrv.iReducaoZ_ECF_Daruma.argtypes = 	[c_char_p, c_char_p]
        self.iDrv.iReducaoZ_ECF_Daruma.restype = c_int
        self.Status = self.iDrv.iReducaoZ_ECF_Daruma(*args);
        return self.Status

    def rAssinarRSA_ECF_Daruma(self, *args):
        """
             pszPathArquivo      A 100 Path e arquivo p gerar Assinatura
             pszPrivateKey       A  20 Path da Chave da Privada(PrivateKey)
             pszAssinaturaGerada A 300 Retorna Assinatura EAD.
        """
        fileToSign = str(args[0]).strip()
        hashEAD = ' '*300
        self.iDrv.rAssinarRSA_ECF_Daruma.argtypes = [c_char_p, c_char_p, c_char_p ]
        self.iDrv.rAssinarRSA_ECF_Daruma.restype = c_int
        self.Status = self.iDrv.rAssinarRSA_ECF_Daruma(fileToSign, hashEAD);
        return (self.Status, hashEAD)

    def rRetornarGTCodificado_ECF_Daruma(self):
        """
          Wrapper dos metodos rRetornarGtCodificado e
              rRetornarNumeroSerieCodificado
          """
        GT = ' ' * 60
        self.iDrv.rRetornarGTCodificado_ECF_Daruma.argtypes = [c_char_p]
        self.iDrv.rRetornarGTCodificado_ECF_Daruma.restype = c_int
        self.Status = self.iDrv.rRetornarGTCodificado_ECF_Daruma(GT);
        if self.Status != 1: return self.Status
        return (self.Status, GT)

