#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.03.06
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import time
import threading


import commdatica
import weiboparser
from weiboparser import WeiboParser
from utils.urlopener import UrlOpener
from utils.logger import Logger

logger = Logger(sys.stderr)

JSONS_COMMENT = 'data/comments.txt'


def load(fname = JSONS_COMMENT):

	if not os.path.exists(fname):
		return []

	fobj = open(fname, 'r')
	comments = []
	for line in fobj:
		comments.append(json.loads(line))

	fobj.close()

	return comments

def downloaded_mids():
	comments = load()

	mids = [] if comments == [] else [comm['mid'] for comm in comments]

	return mids

class ListIterator:
	def __init__(self, data, iter_round = False):
		self.data = data
		self.datalen = len(data)
		self.idx = 0
		self.iter_round = iter_round

		self.lock = threading.Lock()
	
		self.show = False

	def set_show(self, show):
		self.show = show

	def restart(self):
		self.lock.acquire()
		self.idx = 0
		self.lock.release()

	def next(self):
		self.lock.acquire()

		if self.idx == self.datalen:
			if not self.iter_round:
				self.lock.release()
				return None
			else:
				self.idx = 0

		datum = self.data[self.idx]
		self.idx += 1

		self.lock.release()

		return datum

class SharedOutFile:
	def __init__(self, fname, ftype = 'w'):
		self.fobj = open(fname, ftype)
		self.lock = threading.Lock()

	def write(self, line):
		self.lock.acquire()
		self.fobj.write(line)
		self.lock.release()

	def close(self):
		self.fobj.close()

class WeiboLauncher:
	def __init__(self):
		pass

	def load_accounts(self, accounts):
		self.iter_account = ListIterator(accounts, iter_round = True)

	def load_bloginfo(self, bloginfo):
		self.iter_bloginfo = ListIterator(bloginfo)
		self.iter_bloginfo.set_show(True)

	def init_outfile(self, fname, ftype):
		self.outfile = SharedOutFile(fname, ftype)

	def close_outfile(self):
		if self.outfile is not None:
			self.outfile.close()

	def thread_parse(self, interval = 5, thread_name = None):
		flag = True

		wbparser = WeiboParser()

		bloginfo = self.iter_bloginfo.next()
		account = self.iter_account.next()

		flag = not (bloginfo is None or account is None)

		fail_count = 0

		while flag:
			#weibolauncher.thread_parse: 
			logger.info('thread_%s downloading (%s %s)'%(
					thread_name, bloginfo.uid, bloginfo.mid))

			wbparser.set_account(account)
			ret = wbparser.parse(bloginfo.uid, bloginfo.mid)
			
			if ret == None:
				fail_count += 1
				if fail_count > 5:
					print 'fail > 5'
			else:
				comm, ids = ret
				blog = {}
				blog.update(bloginfo.todict())
				blog['comments_count'] = len(comm)
				blog['comments'] = comm
				blog['ids'] = ids

				self.outfile.write(json.dumps(blog) + '\n')

			bloginfo = self.iter_bloginfo.next()
			account = self.iter_account.next()
			
			flag = not (bloginfo is None or account is None)

			if flag:
				time.sleep(interval)
	

	def launch(self, n_instance):
		threads = []

		for i in range(n_instance):
			thread = threading.Thread(target = self.thread_parse, args = (5, i, ))
			thread.start()

			threads.append(thread)
			
		for thread in threads:
			thread.join()

def test():
	all_accounts = weiboparser.load_accounts()
	accounts = all_accounts[:25]


	mids = set(downloaded_mids())
	all_bloginfo = [bloginfo for bloginfo in commdatica.load() if not bloginfo.mid in mids]
	bloginfo = all_bloginfo[:8]

	main(accounts, bloginfo, 4)


def main(accounts, bloginfo, n_instance):
	launcher = WeiboLauncher()
	launcher.load_accounts(accounts)
	launcher.load_bloginfo(bloginfo)
	launcher.init_outfile(JSONS_COMMENT, 'w')
	launcher.launch(n_instance)
	launcher.close_outfile()

if __name__ == '__main__':
	test()

