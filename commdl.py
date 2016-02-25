#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.25
Description: weibo comment downloader
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import shutil

import statica
import weiboparser as wbparser
from utils.logger import Logger
from const import DIR_COMMENTS, N_EMO

logger = Logger()

def download_comments(eids):
	euids = statica.load_euids(eids)
	
	if not os.path.exists(DIR_COMMENTS):
		shutil.makedir(DIR_COMMENTS)

	for eid, uids in euids.items():
		
	

if __name__ == '__main__':
	download_comments(range(N_EMO))
