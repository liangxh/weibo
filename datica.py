#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.25
Modified: 2016.01.25
Description: a tool used to collect data for further experiment
'''

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import zhprocessor
from share import blogger, emotica
from utils import textcleaner

def is_valid(blog):
	'''
	check if the blog 
	'''
	res = extract(blog)
	return not res == None

def extract(blog):
	'''
	analyse the blog, if it contains only one distinct emoticon and the text part is not empty,
	return the text part and emoticon, otherwise None is returned.
	'''

	blog = blog.decode('utf8')
	main_blog = blogger.extract_main(blog)
	emoticons = emotica.extract_emoticons(main_blog)		

	if len(emoticons) == 0:
		#print 'No Emoticons'
		return None

	text = emotica.remove_emoticons(main_blog)
	text = blogger.remove_korean(text)
	text = blogger.remove_space(text)

	if len(text) == 0:
		'''
		no text content
		'''
		#print 'No text'
		return None

	if not zhprocessor.contain_zh(text):
		'''
		no chinese character
		'''
		print text		
		return None

	phrases = [emotica.remove_prefix(emo) for emo in emoticons]
	phrases = set(phrases)
	#print ', '.join(list(phrases))
	if len(phrases) > 1:
		'''
		more than one distinct emoticons within this blog
		'''
		#print 'Too many phrases'
		return None

	emo = emotica.remove_prefix(list(phrases)[0])
	text = re.sub('\s+', ' ', text).strip()
	return text, emo

if __name__ == '__main__':
	t = u' @招商银行 对面的招商银行装修！！油漆味弥漫两天了，大热天关窗[泪][泪][泪]柳州柳钢支行...'
	t = textcleaner.simplify_chinese(t)
	res = extract(t)
	if res == None:
		print 'INVALID'
	else:
		text, emo = res
		print '%s|%s'%(text, emo)
		print [text, ]

