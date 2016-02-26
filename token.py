#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.26
Description: tokenize all the text
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import cPickle

import zhprocessor as zhpr
from const import DIR_TEXT, DIR_TOKEN, N_EMO

def prepare(eids = xrange(N_EMO)):
	if not os.path.exists(DIR_TOKEN):
		os.mkdir(DIR_TOKEN)

	for eid in eids:
		seqs = []
		lines = open(DIR_TEXT + '%d.txt', 'r').read().split('\n')
		for line in lines:
			seqs.append(zhpr.tokenize(line))
		
		cPickle.dump(seqs, open(DIR_TOKEN + '%d.pkl', 'w'))

def load(n_emo = N_EMO):
	eseqs = []

	for eid in xrange(n_emo):
		fname = DIR_TOKEN + '%d.pkl'
		if not os.path.exists(fname):
			print '[warning] %s not found'%(fname)
			return None

		eseqs.append(cPickle.load(open(fname, 'r')))

	return eseqs	

if __name__ == '__main__':
	prepare()
