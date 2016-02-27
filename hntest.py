#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.26
Description: script used to test the coverage the hownet
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import tokenprocessor as tokenpr
from hownet import HowNet
from const import N_EMO, DIR_TEXT, DIR_TOKEN
from utils import progbar
import matplotlib.pyplot as plt

def test(n_emo = N_EMO):
	hownet = HowNet()

	content_all = 0
	content_supported = 0	

	token_all = set()
	token_supported = {}
	
	pbar = progbar.start(n_emo * 4000)

	i = 0

	token_not_supported = {}
	cover_dist = []


	eseqs = tokenpr.load()
	for eid, seqs in enumerate(eseqs):
		for seq in seqs:
			content_all += len(seq)
			
			sup_len = 0
			for token in seq:
				token_all.add(token)
				
				if hownet.support(token):
					sup_len += 1
					content_supported += 1
					if token_supported.has_key(token):
						token_supported[token] += 1
					else:
						token_supported[token] = 1
				else:
					if token_not_supported.has_key(token):
						token_not_supported[token] += 1
					else:
						token_not_supported[token] = 1

			cover_dist.append((len(seq), sup_len))

	

	'''
	for eid in range(n_emo):
		lines =  open(DIR_TEXT + '%d.txt'%(eid), 'r').read().split('\n')
		for line in lines:
			tokens = zhprocessor.tokenize(line)
			n_content += len(tokens)
			for token in tokens:
				token_all.add(token)
				if hownet.support(token):
					content_coverage += 1
					token_supported.add(token)
			i += 1
			pbar.update(i)
	'''

	pbar.finish()

	print 'n_token: %d'%(len(token_all))
	print 'token_coverage: %.1f%%'%(100. * len(token_supported) / len(token_all))
	print 'n_content: %d'%(n_content)
	print 'content_coverage: %.1f%%'%(100. * content_coverage / n_content)


if __name__ == '__main__':
	test(1)
