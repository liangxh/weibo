#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.20
Modified: 2016.01.28
Description: stores const variables for sharing 
'''

DIR_DATA = 'data/'
DIR_OUTPUT = 'output/'
DIR_EID_MIDS = DIR_DATA + 'eid_mids/'

TXT_EID = DIR_DATA + 'eid.txt'
TXT_STATUS_COUNT = DIR_DATA + 'status_count.txt'
PKL_REPORT = DIR_DATA + 'report.pkl'

JSON_EMO = DIR_DATA + 'emoticon.json'
URL_EMO = 'http://weibo.com/aj/mblog/face?type=face&_wv=5&ajwvr=6&__rnd=1453464129146'

WEIBO_COOKIE = open(DIR_DATA + 'weibo_cookie.txt', 'r').read()
WEIBO_MYID = '1784127181'

STATUS_COUNT_MAX = 1000
STATUS_COUNT_2ND = 1098

TOTAL_USERS = 1666637
TOTAL_BLOGS = 156365006

PKL_EMO_MIDS = DIR_DATA + 'emo_mids.pkl'
