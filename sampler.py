#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.04
Modified: 2016.02.04
Description: filter text for certain emoticon
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import cPickle
from const import DIR_EID_MID_UID

def muid2umids(mid_uid):
	'''
	transfer {mid: uid, ...} to {uid: [mid, mid, ...], ...}
	'''

	uid_mids = {}

	for mid, uid in mid_uid.items():
		if uid_mids.has_key(uid):
			uid_mids[uid].append(mid)
		else:
			uid_mids[uid] = [mid, ]

	return uid_mids

def load_mid_uid(eid):
	'''
	load {mid:uid, ...} from data/eid_mid_uid/$EID.pkl
	'''

	fname = DIR_EID_MID_UID + '%d.pkl'%(eid)
	
	if not os.path.exists(fname):
		print '[Warning] %s not found'%(fname)
		return None

	return cPickle.load(open(fname, 'r'))

def analyse_mid_uid(eid):
	mid_uid = load_mid_uid(eid)

	umids = muid2umids(mid_uid)
	
	uid_mids = sorted(umids.items(), key = lambda k: -len(k[1]))

	c = 0
	target = 4000

	for i, item in enumerate(uid_mids):
		uid, mids = item
		print '%d. %d'%(i + 1, len(mids))

		n_mids = len(mids)
		
		if n_mids > 100:
			c += 100
		else:
			c += n_mids
		
		if c >= target:
			break

	coverage = 100.
	if c < target:
		coverage = 100. * c / target
	
	print '==================================='
	print 'coverage: %0.2f%%'%(coverage)

def sample_text(eid):
	import db
	con = db.connect()
	cur = con.cursor()

	mid_uid = load_mid_uid(eid)
	umids = muid2umids(mid_uid)
	
	uid_mids = sorted(umids.items(), key = lambda k: -len(k[1]))

	c = 0
	target = 4000

	texts = []
	for i, item in enumerate(uid_mids):
		uid, mids = item
		
		if len(mids) > 100:
			mids = mids[:100]
		
		for mid in mids:
			cur.execute('SELECT text FROM microblogs WHERE user_id=%s AND mid=%s LIMIT 1'%(uid, mid))
			text = cur.fetchone()[0]
			texts.append(text)

		c += len(mids)
		if c >= target:
			break
	
	open('output/%d.txt'%(eid), 'w').write('\n'.join(texts))

if __name__ == '__main__':
	#analyse_mid_uid(0)
	sample_text(0)

