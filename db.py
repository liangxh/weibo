
#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.20
Modified: 2016.01.27
Description: a script for access to mysql.weibo
'''

import MySQLdb as db

con = None

def connect():
	if con:
		return con

	try:
		con = db.connect('localhost', 'weiboguest', 'weiboguest', 'weibo')
		return con
	except db.Error, e:
		print 'MySQL: [ERRNO %d] %s'%(e.args[0], e.args[1])
		return None
