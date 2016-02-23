#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.24
Modified: 2016.01.24
Description: a tool used to process Weibo
'''

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

pattern_korean = re.compile(u'[\u1100-\u11ff\u2e80-\u33ff\uac00-\ud7af\u3130–\u318f\u3200–\u32ff\ua960–\ua97f\uac00-\ud7a3\ud7b0–\ud7ff\uff00–\uffef]+')

def extract_main(blog):
	text = remove_forward(blog)
	text = remove_share(text)
	text = remove_mention(text)

	text = remove_space(text)	

	return text

def remove_space(text):
	text = text.strip()
	text = re.sub('\s+', ' ', text)

	return text

def remove_korean(text):
	return re.sub(pattern_korean, ' ', text)

def remove_forward(blog):
	return re.sub('//@.+$', '', blog, re.DOTALL)

def remove_share(blog):
	text = re.sub(u'【[^】]+】.*http://t.cn/\w+', '', blog, re.DOTALL)
	text = re.sub(u'(\s+\S+:)?http://t.cn/\w+\s*$', '', text)
	text = re.sub(u'^.*http://t.cn/\w+\s+（\S+自 @\S+）', '', text, re.DOTALL)

	return text

def remove_mention(blog):
	return re.sub('@\S+', '', blog)

if __name__ == '__main__':
	blog = u'【重庆回应长江水变红：未测出有毒物质】核心提示：9月7日，重庆环保局回应长江变“红河”称，河水中未检测出有毒有害物质，河水变红系水中铁离子含量过高所致。... http://t.cn/zWDrb4x  [哈哈]富含铁离子，还富含各种矿物质和维生素，这不是高级纯天然矿泉水吗，环保菊长先来一口？'
	print extract_main(blog)
