#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.09
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re

import jieba
from jieba import posseg

jieba.initialize()
jieba.enable_parallel(4)

re_zh = u'\u4e00-\u9fa5'
pattern_not_zh = re.compile(u'[^%s]+'%(re_zh))

def extract(text):
	try:
		text = text.decode('utf8')
	except:
		print '[Warning] cannot convert to UTF-8: ', text
	
	text = re.sub(pattern_no_zh, ' ', text)
	return text

def segment(text, pos_tagging = False):
	if pos_tagging:
		return posseg.cut(text)
	else:
		return jieba.cut(text)

def tokenize(text):
	words = segment(text, True)
	tokens = []
	for w in words:
		if not w.flag == 'x':
			tokens.append(w.word)

	return tokens

if __name__ == '__main__':
	text = u'我爱北京天安门'

	words = segment(text)
	print '/'.join(words)

	words = segment.cut(text, True)
	for w in words:
		print w.word, w.flag

