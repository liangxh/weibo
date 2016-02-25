#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.25
Description: weibo comment downloader
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import shutil
import time
import json

import statica
import weiboparser as wbparser

from const import DIR_COMMENTS, N_EMO
from utils.logger import Logger

logger = Logger()

def download_comments(eids, interval = 10):
	euids = statica.load_uids(eids)
	
	if not os.path.exists(DIR_COMMENTS):
		os.mkdir(DIR_COMMENTS)

	missing = []
	for eid, uids in sorted(euids.items(), key = lambda k:k[0]):
		downloaded_mid = set()
		fname = DIR_COMMENTS + '%d.jsons'%(eid)

		if os.path.exists(fname):
			fobj = open(fname, 'r')
			for line in fobj:
				downloaded_mid.append(json.loads(line)['mid'])
			fobj.close()

		fobj = open(fname, 'a')

		n_loops = len(uids) - len(downloaded_mid)
		loop = 0

		for mid, uid in uids.items():
			start_time = time.time()

			if not mid in download_mid:
				res = wbparser.get(uid, mid, show_result = True)
				if res == None:
					logger.warning('failed to download comments of (uid, mid) = (%s, %s)'%(uid, mid))
					missing.append((eid, mid, uid))
				else:
					comm, ids = res
					fobj.write(json.dumps({'uid':uid, 'mid':mid, 'comm':comm, 'ids':ids}) + '\n')
				loop += 1			

			end_time = time.time()

			logger.info('EID = %d, LOOP = %d / %d (%.1f sec)'%(loop, n_loop, end_time - start_time))
			time.sleep(interval)
			
		fobj.close()
		break
	
	fobj = open('missing_comm.txt', 'w')
	for eid, mid, uid in missing:
		fobj.write('%d %s %s\n'%(eid, mid, uid))
	fobj.close()

if __name__ == '__main__':
	download_comments(range(N_EMO))

