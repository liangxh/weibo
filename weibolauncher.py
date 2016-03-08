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
	'''
	load all the comments downloaded and saved in JSONS_COMMENT
	'''

	if not os.path.exists(fname):
		return []

	fobj = open(fname, 'r')
	comments = []
	for line in fobj:
		comments.append(json.loads(line))

	fobj.close()

	return comments

def downloaded_mids():
	'''
	get the list of mids from JSONS_COMMENT
	which are the mids of the blogs whose comments have been downloaded
	'''

	comments = load()

	mids = [] if comments == [] else [comm['mid'] for comm in comments]

	return mids

class ListIterator:
	'''
	an iterator for multi-threading
	'''

	def __init__(self, data, iter_round = False):
		self.data = data
		self.datalen = len(data)
		self.idx = 0
		self.iter_round = iter_round

		self.lock = threading.Lock()
	
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
	'''
	a write file with threading lock though I don't know if it is necessary
	'''

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
	'''
	a launcher for parsing weibo comments by multi-threading
	'''

	def __init__(self):
		pass

	def load_accounts(self, accounts):
		'''
		initialize a round iterator for accounts
		'''
		self.iter_account = ListIterator(accounts, iter_round = True)

	def load_bloginfo(self, bloginfo):
		'''
		initialize a iterator for bloginfos
		'''
		self.iter_bloginfo = ListIterator(bloginfo)

	def init_outfile(self, fname, ftype):
		'''
		initialize a output file object for threading
		'''
		self.outfile = SharedOutFile(fname, ftype)

	def close_outfile(self):
		'''
		close the output file
		'''
		if self.outfile is not None:
			self.outfile.close()

	def thread_parse(self, interval = 5, thread_name = None):
		'''
		an instance for parseing weibo comments
		which sleep for $interval seconds between every loop
		'''

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
		'''
		parse weibo comments by $n_instance threads
		accounts and bloginfo must be initialized by init_account and init_bloginfo in advance
		'''

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

	all_bloginfo = commdatica.load()
	
	# do not download comments for the same blog again
	mids = set(downloaded_mids())
	filtered_bloginfo = [bloginfo for bloginfo in all_bloginfo if not bloginfo.mid in mids]

	bloginfo = filtered_bloginfo[:8]

	main(accounts, bloginfo, 4)


def main(accounts, bloginfo, n_instance):
	launcher = WeiboLauncher()
	launcher.load_accounts(accounts)
	launcher.load_bloginfo(bloginfo)
	launcher.init_outfile(JSONS_COMMENT, 'a')
	launcher.launch(n_instance)
	launcher.close_outfile()

if __name__ == '__main__':
	test()

