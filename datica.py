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

from share import blogger, emotica
from utils import textcleaner

def is_space(text):
	'''
	check if the text is composed of space
	'''
	m = re.match('^\s+$', text)
	return not m == None

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

	main_blog = blogger.extract_main(blog)

	if is_space(main_blog):
		'''
		no text content
		'''
		return None

	emoticons = emotica.extract_emoticons(main_blog)
	text = emotica.remove_emoticons(main_blog)
	if len(emoticons) == 0 or is_space(text):
		'''
		no text content or no emoticon within this blog
		'''
		return None

	phrases = [emotica.remove_prefix(emo) for emo in emoticons]
	phrases = set(phrases)
	#print ', '.join(list(phrases))
	if len(phrases) > 1:
		'''
		more than one distinct emoticons within this blog
		'''
		return None

	emo = emotica.remove_prefix(list(phrases)[0])
	text = re.sub('\s+', ' ', text).strip()
	return text, emo

if __name__ == '__main__':
	t = u'四核旗舰对决 十款热门手机对比导购 http://t.cn/zWcJdvt  （分享自 @新浪科技） 有什么能取代我的大5230？[哈哈]'
	t = textcleaner.simplify_chinese(t)
	res = extract(t)
	if res == None:
		print 'INVALID'
	else:
		text, emo = res
		print '%s|%s'%(text, emo)

