#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.03.04
Description: a script used to analyse umcomm.txt
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from utils import progbar

class BlogInfo:
	def __init__(self, uid, mid, text, comments_count):
		self.uid = uid
		self.mid = mid
		self.text = text
		self.comments_count = comments_count

	def todict(self):
		return {'uid':self.uid, 'mid':self.mid, 'text':self.text, 'comments_count':self.comments_count}

FNAME_BLOGS_RAW = 'data/blogs_400000.txt'
FNAME_BLOGS_FILTERED = 'data/blogs_subset.txt'  

def prepare():
	'''
	load data/blogs_400000.txt and after filtering by blogger.is_valid
	those which pass are saved into data/blogs_subset.txt
	'''

	import blogger
	from utils import progbar
	blogs = []

	lines = open(FNAME_BLOGS_RAW, 'r').readlines()
	
	pbar = progbar.start(len(lines))
	for i, l in enumerate(lines):
		parts = l[:-1].decode('utf8').split('\t')
		params = []
		for part in parts:
			if not part == '':
				params.append(part)

		text = params[2]
		res = blogger.extract(text)
		
		if res is not None:
			uid = params[0]
			mid = params[1]
			comments_count = int(params[3])

			blogs.append(BlogInfo(uid, mid, text, comments_count))
		
		pbar.update(i + 1)
	pbar.finish()

	fobj = open(FNAME_BLOGS_FILTERED, 'w')
	for blog in blogs:
		fobj.write('%s\t%s\t%s\t%d\n'%(blog.uid, blog.mid, blog.text, blog.comments_count))
	fobj.close()

def load():
	'''
	load data/blogs_subset.txt as list of BlogInfo
	'''

	lines = open(FNAME_BLOGS_FILTERED, 'r').readlines()
	blogs = []	

	pbar = progbar.start(len(lines))
	for i, l in enumerate(lines):
		params = l[:-1].split('\t')
		uid = params[0]
		mid = params[1]
		text = params[2]
		comments_count = int(params[3])
		blogs.append(BlogInfo(uid, mid, text, comments_count))
		
		pbar.update(i + 1)

	pbar.finish()

	return blogs

def tohist(ls):
	hist = {}
	for l in ls:
		if hist.has_key(l):
			hist[l] += 1
		else:
			hist[l] = 1
	return hist

def test():
	import matplotlib.pyplot as plt

	blogs = load()
	n_blogs = len(blogs)

	print '################## Distribution of users #############################'

	uids = [blog.uid for blog in blogs]
	ucount = tohist(uids).values()

	uhist = tohist(ucount)
	uhist = sorted(uhist.items(), key = lambda k:k[0])
	for k, v in uhist[:10]:
		print '%d (%d, %.2f%%)'%(k, v, 100.*v / n_blogs)

	k, v = uhist[-1]
	print '...\n%d (%d, %.2f%%)'%(k, v, 100.*v / n_blogs)

	plt.figure()
	plt.hist(ucount, 50, alpha = 0.75)
	plt.savefig('output/new_udist.png')

	print '################### Distribution of comments_count #################'

	commcount = [blog.comments_count for blog in blogs]
	chist = tohist(commcount)
	chist = sorted(chist.items(), key = lambda k:k[0])
	for k, v in chist:
		print '%d (%d, %.2f%%)'%(k, v, 100.*v / n_blogs)

	k, v = chist[-1]
	print '...\n%d (%d, %.2f%%)'%(k, v, 100.*v / n_blogs)

	plt.figure()
	plt.hist(commcount, 50, alpha = 0.75)
	plt.savefig('output/new_cdist.png')

if __name__ == '__main__':
	test()