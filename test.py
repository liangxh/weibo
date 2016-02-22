#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.09
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import zhprocessor
import datica
from share import emotica, blogger

lines = open('output/0.txt', 'r').read().split('\n')
for line in lines[:100]:
	line = line.decode('utf8')
	res = datica.extract(line)
	if res == None:
		print '###############################'
		print 'None: ', line
		continue

	text, emo = res	

	print '###############################'
	print 'text: ', text
	print 'emo: ', emo
	print 'tokens: ', '/'.join(zhprocessor.tokenize(text))
