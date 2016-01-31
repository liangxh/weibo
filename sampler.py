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

	emoticons = []
	for text, comments_count in cur:
		res = datica.extract(text)
		if not res == None:
			text, emoticon = res
			emoticons.append(emoticon)

			valid_count += 1
			if comment_count > 0:
				comment_count += 1

	emoticons = tohist(emoticons)
	emoticons = sorted(emoticons.items(), key = lambda k: -k[1])
	top_emotions = emoticons[:3] if len(emoticons) > 3 else emoticons	

	report = ''
	report += '# of valid blogs: %d\n'%(valid_count)
	report += '# of blogs with comments: %d\n'%(comment_count)
	report += '# of emoticons: %d\n'%(len(emoticons))
	report += 'top 3 (or less) emoticons: %s\n'%(', '.join(['%s(%d)'%(k, v) for k, v in top_emoticons]))
		
	print report 

def sampling():
	status_count = get_status_count()
	hlist_count = tohlist(status_count)

	sorted_items = sorted(hlist_count.items(), key = lambda k: - len(k[1]))
	uid = sorted_items[0][1][0]

	report(sorted_items[0][1][0])
	report(sorted_items[0][1][1])
	report(sorted_items[0][1][2])
	

if __name__ == '__main__':
	sampling()

