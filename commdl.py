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
import traceback

import datica
import weiboparser as wbparser

from const import DIR_COMMENTS, N_EMO
from utils.logger import Logger

logger = Logger()

def download_comments(eids, interval = 10):
	euids = datica.load_euids(eids)
	
	if not os.path.exists(DIR_COMMENTS):
		os.mkdir(DIR_COMMENTS)

	missing = []
	for eid, uids in sorted(euids.items(), key = lambda k:k[0]):
		downloaded_mid = set()
		fname = DIR_COMMENTS + '%d.jsons'%(eid)

		if os.path.exists(fname):
			fobj = open(fname, 'r')
			for line in fobj:
				downloaded_mid.add(json.loads(line)['mid'])
			fobj.close()
			logger.info('comments of %d blogs with EID = %d have already been downloaded'%(
					len(downloaded_mid), eid)
				)

		fobj = open(fname, 'a')

		n_loops = len(uids.items()) - len(downloaded_mid)
		loop = 0

		for mid, uid in uids.items():
			if not mid in downloaded_mid:
				start_time = time.time()

				logger.info('downloading (eid, uid, mid) = (%d, %s, %s)'%(eid, uid, mid))
				try:
					res = wbparser.get(uid, mid, show_result = True)
				except KeyboardInterrupt:
					continue
				except:
					logger.error('failed to save comments: %s'%(traceback.format_exc()))
					res = None

				end_time = time.time()

				if res == None:
					logger.info('EID = %d, LOOP = %d / %d failed (%.1f sec)'%(
							eid, loop, n_loops, end_time - start_time
						))
					missing.append((eid, mid, uid))
				else:
					comm, ids = res
					
					if len(comm) == 0:
						logger.warning('EID = %d, LOOP = %d / %d, NO comments (%.1f sec)'%(
								eid, loop, n_loops, len(comm), end_time - start_time
							)
					else:
						fobj.write(json.dumps({'uid':uid, 'mid':mid, 'comm':comm, 'ids':ids}) + '\n')
						logger.info('EID = %d, LOOP = %d / %d, %d comments (%.1f sec)'%(
								eid, loop, n_loops, len(comm), end_time - start_time
							))
				loop += 1
				time.sleep(interval)
			
		fobj.close()
	
	fobj = open('missing_comm.txt', 'w')
	for eid, mid, uid in missing:
		fobj.write('%d %s %s\n'%(eid, mid, uid))
	fobj.close()

def download_comment(eid, uid, mid):
	fname = DIR_COMMENTS + '%d.jsons'%(eid)
	
	if os.path.exists(fname):
		downloaded_mid = set()

		fobj = open(fname, 'r')
		for line in fobj:
			downloaded_mid.add(json.loads(line)['mid'])
		fobj.close()
		logger.info('comments of %d blogs with EID = %d have already been downloaded'%(
				len(downloaded_mid), eid)
			)
		
		if mid in downloaded_mid:
			logger.warning('comments of MID %s has been downloaded'%(mid))
			return		

	fobj = open(fname, 'a')

	start_time = time.time()

	logger.info('downloading (eid, uid, mid) = (%s, %s, %s)'%(eid, uid, mid))
	try:
		res = wbparser.get(uid, mid, show_result = True)
	except KeyboardInterrupt:
		pass
	except:
		logger.error('failed to save comments: %s'%(traceback.format_exc()))
		res = None
		end_time = time.time()

		if res == None:
			logger.info('EID = %d, LOOP = %d / %d failed (%.1f sec)'%(
				eid, loop, n_loops, end_time - start_time
				))
			missing.append((eid, mid, uid))
		else:
			comm, ids = res
			fobj.write(json.dumps({'uid':uid, 'mid':mid, 'comm':comm, 'ids':ids}) + '\n')
			logger.info('EID = %d, LOOP = %d / %d (%s %s) %d comments (%.1f sec)'%(
					eid, loop, n_loops, uid, mid, len(comm), end_time - start_time
				))

	fobj.close()

if __name__ == '__main__':
	download_comments(range(N_EMO))
	

