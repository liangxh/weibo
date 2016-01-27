import MySQLdb as db

def connect():
	try:
		con = db.connect('localhost', 'weiboguest', 'weiboguest', 'weibo')
		return con
	except db.Error, e:
		print 'MySQL: [ERRNO %d] %s'%(e.args[0], e.args[1])
		return None
