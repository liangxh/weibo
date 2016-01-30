#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.29
Modified: 2016.01.29
Description: 
'''

#import db
from const import TXT_STATUS_COUNT
from utils import timer

def tohist(ls):
	hist = {}
	for l in ls:
		if not hist.has_key(l):
			hist[l] = 1
		else:
			hist[l] += 1

	return hist

def tohlist(hist):
	hlist = {}
	for k, v in hist.items():
		if hlist.has_key(v):
			hlist[v].append(k)
		else:
			hlist[v] = [k, ]

	return hlist

def get_status_count():
	fobj = open(TXT_STATUS_COUNT, 'r')
	lines = fobj.read().split('\n')
	fobj.close()

	status_count = {}
	for line in lines:
		args = line.split(' ')
		status_count[args[0]] = int(args[1])

	return status_count

@timer()
def report(uid):
	import db
	import datica

	con = db.connect()
	cur = con.cursor()
	cur.execute('SELECT text, comments_count FROM microblogs WHERE user_id=%s'%(uid))

	valid_count = 0
	comment_count = 0
	for text, comments_count in cur:
		if datica.is_valid(text):
			valid_count += 1

		if comment_count > 0:
			comment_count += 1

	report = ''
	report += 'VALID: %d\n'%(valid_count)
	report += 'HAS_COMMENT: %d\n'%(comment_count)
	print report 

def sampling():
	status_count = get_status_count()
	hlist_count = tohlist(status_count)

	sorted_items = sorted(hlist_count.items(), key = lambda k: - len(k[1]))
	uid = sorted_items[0][1][0]

	report(uid)

if __name__ == '__main__':
	sampling()

