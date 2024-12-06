
from datetime import datetime
import logging

class Logger(object):
	""" This logger will handle the exception logging ane other messages logging. 
		We use this 'singleton' class to make it easy to write to the log file.
		To configure the logger use Logger.SetLoggingpath(...) , to use the logger Logger.GetInstance().LogMessage(...) """

	_LoggingPath = None
	_Instance = None

	@classmethod
	def SetLoggingpath(cls,logpath):
		cls._LoggingPath = logpath


	@classmethod
	def GetInstance(cls):
		if (cls._Instance == None):
			cls._Instance = Logger()
		return cls._Instance
	def __init__(self):
		pass

	def LogMessage(self,text):
		if (Logger._LoggingPath != None):
			with open(Logger._LoggingPath,"a") as logstream:
				logstream.write(f"{datetime.now()} => {text}\n")
				
	def LogException(self,ex):
		self.LogMessage(f"{ex}")
		raise ex
		
		