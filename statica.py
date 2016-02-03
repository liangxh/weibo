#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.03
Modified: 2016.02.03
Description: create statistics report from mysql
'''

import cPickle

import db, datica
from const import TOTAL_BLOGS, PKL_EMO_MIDS
from utils import progbar

def collect_emo_mid():
	con = db.connect()
	cur = con.cursor()
	cur.execute('SELECT mid, text FROM microblogs')
	
	pbar = progbar.start(TOTAL_BLOGS)
	loop = 0
	
	emo_mids = {}

	for mid, text in cur:
		res = datica.extract(text)
		if res == None:
			continue
		
		text, emo = res
		if emo_mids.has_key(emo):
			emo_mids[emo].append(mid)
		else:
			emo_mids[emo] = [mid, ]
	
		loop += 1
		pbar.update(loop)

	pbar.finish()

	cPickle(emo_mids, PKL_EMO_MIDS)

if __name__ == '__main__':
	collect_emo_mid()


