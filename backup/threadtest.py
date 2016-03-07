#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
'''

import time
import threading
fobj = open('a.txt', 'w')
lock = threading.Lock()


def appender(tid):
	global fobj

	for i in range(5):
		time.sleep(0.5)
		lock.acquire()
		fobj.write('thread %d\n'%(tid))
		lock.release()

threads = []
for i in range(5):
	t = threading.Thread(target = appender, args = (i, ))
	threads.append(t)
	t.start()

for t in threads:
	t.join()

print 'all finished'

