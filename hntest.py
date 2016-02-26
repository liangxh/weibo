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

import zhprocessor
from hownet import HowNet
from const import N_EMO, DIR_TEXT
from utils import progbar

def test(n_emo = N_EMO):
	hownet = HowNet()

	n_content = 0
	n_token = 0
	content_coverage = 0	

	token_all = set()
	token_supported = set()
	
	pbar = progbar.start(n_emo * 4000)
	i = 0
	
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

	pbar.finish()

	print 'n_token: %d'%(len(token_all))
	print 'token_coverage: %.1f%%'%(100. * len(token_supported) / len(token_all))
	print 'n_content: %d'%(n_content)
	print 'content_coverage: %.1f%%'%(100. * content_coverage / n_content)


if __name__ == '__main__':
	test()
