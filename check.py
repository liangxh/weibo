#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv) < 2:
	eid = 0
else:
	eid = int(sys.argv[1])

import datica
import zhprocessor as zhp

fname = 'output/text_%d.txt'%(eid)
lines = open(fname, 'r').read().split('\n')

for l in lines:
	res = datica.extract(l)
	#if res == None:
		#print l
'''

from share import blogger
text = u'ㅋㅋ아아!!종대최고!!!!![泪][泪][泪] //@________yoon:깜짝이야ㅋㅋㅋ 갑자기 왜 转发되나 했네ㅋㅋ 종대가 대표로 가위바위보해서 팬 네명 남을때 까지 해서 최후의 4인 했음ㅋㅋ //@李孛蓓三杯倒T-T:언니!!!!!!!!ㅜ대박!!!!![泪][泪][泪][泪][泪][泪][泪][泪][泪]부러웡..힝..ㅠㅠ'
t = blogger.remove_korean(text)
print t

'''

