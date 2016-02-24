#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.23
Description: datica for processing uni-code dataset
'''

import os
import cPickle
from tfcoder import TfCoder
from const import DIR_TEXT, PKL_TFDATA, PKL_TFCODER, N_EMO

def prepare():
	'''
	prepare data for LSTM
	data are structured as [[codes, codes, ...], ...], which are ordered by eid
	'''

	import blogger	
	from utils import progbar

	coder = cPickle.load(open(PKL_TFCODER, 'r'))

	datalist = []

	pbar = progbar.start(N_EMO)
	for eid in range(N_EMO):
		lines = open(DIR_TEXT + '%d.txt'%(eid), 'r').read().split('\n')
		data = []
		for line in lines:
			text, emo = blogger.extract(line)
			codes = coder.code(text)
			data.append(codes)
		datalist.append(data)
		pbar.update(eid + 1)

	pbar.finish()

	cPickle.dump(datalist, open(PKL_TFDATA, 'w'))

def load():
	'''
	load data as [[codes, codes, ...], ...] from PKL_TFDATA
	return None if something is wrong
	'''

	if not os.path.exists(PKL_TFDATA):
		print 'unidatica.load: [Remind] please prepare() the dataset before trying to load() it'
		return None

	try:
		return cPickle.load(open(PKL_TFDATA, 'r'))
	except:
		print 'unidatica.load: [Error] failed to load %s'%(PKL_TFDATA)
		return None

if __name__ == '__main__':
	prepare()

