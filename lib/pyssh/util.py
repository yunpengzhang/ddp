#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging

logger = logging.getLogger( "pyssh" )

def getLocalUser():
	try:
		import getpass
		localUser = getpass.getuser()
		return localUser
	except:
		logger.exception('exception when getting local current login user')
		return None

def getLocalIP(ifName):
	try:
		import socket
		import struct
		import fcntl
		s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ifName[:15]))[20:24])
	except:
		logger.exception('getIP exception for intf:%s', ifName)
		return None


def isLocalPathExists(localPath):
	try:
		import os
		return os.path.exists(localPath)
	except:
		logger.exception('exception, test exists for local path:%s', localPath)
		return False


def isDirOfLocalPath(localPath):
	try:
		import os
		return os.path.isdir(localPath)
	except:
		logger.exception('exception, test whether dir or not for local path:%s', localPath)
		return False


def createTempFileInLocal(tempDir='/tmp', tryTimes=10):
	### create source temp file in local host ###
	import os
	import random

	tryCounter = 0
	while True:
		if tryTimes < tryCounter:
			logger.error('can not create temp file in local, because of no proper temp name')
			return {'code':-8003, 'output':'can not create temp file in local, because of no proper temp name'}
		sourceTempFileName = ''.join( random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 25) )
		sourceTempFilePath = os.path.join(tempDir, sourceTempFileName)
		if os.path.exists( sourceTempFilePath ):
			tryCounter += 1
		else:
			break
	try:
		sourceTempFile = open(sourceTempFilePath, 'w')
		sourceTempFile.write('temp file')
		#sourceTempFile.flush()
		sourceTempFile.close()
		logger.debug('create temp file in local, success:%s', sourceTempFilePath)
		return {'code':0, 'path':sourceTempFilePath, 'name':sourceTempFileName}
	except:
		logger.exception('exception when writing temp file in local, temp file:%s', sourceTempFilePath)
		return {'code':-8004, 'output':'can not create temp file in local, because of writing error'}


def deleteFileInLocal(localFilePath):
	### delete local temp file
	try:
		import os
		os.remove( localFilePath )
		return True
	except:
		return False


