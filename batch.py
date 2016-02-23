#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tarfile
import sampler

for i in range(100):
	sampler.sample_text(i)

tar = tarfile.open('output/tmp.tar', 'w')
for i in range(100):
	f1 = 'output/text_%d.txt'%(i)
	f2 = 'output/text_%d.txt'%(i)
	tar.add(f1)
	tar.add(f2)

tar.close()
