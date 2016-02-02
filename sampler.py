#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.29
Modified: 2016.01.29
Description: 
'''

#import db

import cPickle
from const import TXT_STATUS_COUNT, PKL_REPORT
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
def analyse(uid):
	import db
	import datica

	con = db.connect()
	cur = con.cursor()
	cur.execute('SELECT text, comments_count FROM microblogs WHERE user_id=%s'%(uid))

	valid_count = 0
	comm_count = 0

	emoticons = []
	for text, comments_count in cur:
		res = datica.extract(text)
		if not res == None:
			text, emoticon = res
			emoticons.append(emoticon)

			valid_count += 1
			if comments_count > 0:
				comm_count += 1

	emoticons = tohist(emoticons)
		
	return valid_count, comm_count, emoticons

def sampling():
	status_count = get_status_count()
	hlist_count = tohlist(status_count)

	sorted_items = sorted(hlist_count.items(), key = lambda k: - len(k[1]))
	
	sample_items = []
	sample_items.extend(sorted_items[0][1])

	valid_list = []
	comm_list = []
	emo_tf = {}
	emo_df = {}

	for uid in sample_items:
		valid_count, comm_count, emos = analyse(uid)
		
		valid_list.append(valid_count)
		comm_list.append(comm_count)
		
		for emo, count in emos:
			if emo_tf.has_key(emo):
				emo_tf[emo] += count
				emo_df[emo] += 1
			else:
				emo_tf[emo] = count
				emo_df[emo] = 1

	valid_hist = tohist(valid_list)
	comm_hist = tohist(comm_list)

	cPickle.dump((valid_hist, comm_hist, emo_tf, emo_df), open(PKL_REPORT, 'w'))

def report2graph():
	valid_hist, comm_hist, emo_tf, emo_df = cPickle(open(PKL_REPORT, 'r'))
	

if __name__ == '__main__':
	sampling()

