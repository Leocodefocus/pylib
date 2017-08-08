#!/usr/bin/python
#!-*-coding:utf-8-*-
import logging.handlers
class selflog:
	logger = None
	levels = {
			"n":logging.NOTSET,
			"d":logging.DEBUG,
			"i":logging.INFO,
			"w":logging.WARN,
			"e":logging.ERROR,
			"c":logging.CRITICAL
		}
	log_level = "d"
	log_file = "history.log"
	log_max_byte = 1024*1024*1024
	log_backup_count = 5
	def __init__(self,filename):
		self.log_file=filename
	#@staticmethod
	def getLogger(self):
		if selflog.logger is not None:
			return selflog.logger
		#logger object created
		selflog.logger = logging.Logger("loggingmodule.selflog")
		#log output fmt
		log_handler = logging.handlers.RotatingFileHandler(filename=self.log_file,\
														maxBytes = selflog.log_max_byte,\
														backupCount = selflog.log_backup_count)
		#log info format
		log_fmt = logging.Formatter("[%(levelname)s][%(funcName)s][%(lineno)d][%(asctime)s]%(message)s")
		log_handler.setFormatter(log_fmt)
		#add logger handler
		selflog.logger.addHandler(log_handler)
		#set logger level
		selflog.logger.setLevel(selflog.levels.get(selflog.log_level))
		return selflog.logger
