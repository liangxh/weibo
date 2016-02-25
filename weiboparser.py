#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.01.25
Modified: 2016.01.25
Description: parse data from Weibo
'''

import re
import time
import json
import traceback

import urllib
import urllib2
urllib2.ProxyHandler({})

from bs4 import BeautifulSoup
from const import WEIBO_COOKIE, WEIBO_MYID

RETCODE = 6102

request_header = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch', 
	'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
	'Connection':'keep-alive', 
	'Cookie':WEIBO_COOKIE,
	#'Host':'weibo.com',
	#'Upgrade-Insecure-Requests':1,
	#'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
}

import StringIO, gzip
def decompress(data):
	'''
	decompress the response package
	'''
	compressedstream = StringIO.StringIO(data)  
	gziper = gzip.GzipFile(fileobj = compressedstream)    
	content = gziper.read()
	return content


def url_search(uid, start_time, key_word):
	'''
	return the url for searching blog, not used 
	'''

	url = 'http://weibo.com/p/100505%s/home'%(uid)

	start_timestamp = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
	end_time = time.strftime('%Y-%m-%d', time.localtime(start_timestamp + 86400))

	params = {
		'pids':'Pl_Official_MyProfileFeed__24',
		'is_ori':1,
		'is_forward':1,
		'is_text':1,
		'is_pic':1,
		'is_video':1,
		'is_music':1,
		'key_word':key_word,
		'start_time':start_time,
		'end_time':end_time,
		'is_search':1,
		'is_searchadv':1,
		'ajaxpagelet':1,
		'ajaxpagelet_v6':1,
		'__ref':'/p/100505%s/home'%(uid),
		'_t':'FM_145372470006591',
	}

	param = urllib.urlencode(params)
	return '%s?%s'%(url, param)

def url_comment(uid, mid):
	'''
	return the url for a small comment list
	'''

	url = 'http://weibo.com/aj/v6/comment/small'

	params = {
		'ajwvr':6,
		'act':'list',
		'mid':mid,
		'uid':WEIBO_MYID,
		'isMain':True,
		'dissDataFromFeed':'[object Object]',
		'ouid':uid,
		'location':'page_100505_home', #???
		'comment_type':1,
		'_t':0,
		'__rnd':0,	#1453814722537
		'retcode':RETCODE,
	}

	param = urllib.urlencode(params)
	return '%s?%s'%(url, param)

def url_comment_page(page, comm_id, max_id):
	'''
	return the url for a comment page
	'''

	url = 'http://weibo.com/aj/v6/comment/big'

	params = {
		'ajwvr':6,
		'id':comm_id,
		'max_id':max_id,
		'page':page,
		'__rnd':0, #1453883315616
		'retcode':RETCODE,
	}

	param = urllib.urlencode(params)
	return '%s?%s'%(url, param)

def request(url):
	'''
	send request to URL with header $request_header
	'''
	req = urllib2.Request(url, headers = request_header)

	try:
		response = urllib2.urlopen(req)
		content = response.read()

		content_type = response.headers.get('content-type')
		#if content_type == 'gzip':
		#	content = zlib.decompress(content)
		content = decompress(content)
		return content
	except urllib2.URLError, e:
		print e.reason
		return None
	except urllib2.HTTPError, e:
		print '[ERRNO %d] %s'%(e.code, e.reason)
		return None

def soup2comments(soup):
	'''
	private function called by $get_comments
	extract comments from soup of the response 
	'''

	comment_list = soup.find('div', attrs={'class':'list_ul'})

	divs_comment = comment_list.findAll('div', attrs={'comment_id':re.compile(r'\d+')})
	comments = []

	for div_comment in divs_comment:
		wb_text = div_comment.find('div', attrs={'class':'WB_text'})

		m = re.match(u'^\s*([^：]+)：(.*)$', wb_text.text, re.DOTALL)
		from_name = m.group(1)
		text = m.group(2)
		to_name = None

		m = re.match(u'回复@([^:]+):(.*)', text, re.DOTALL)
		if m:
			to_name = m.group(1).strip()
			text = m.group(2).strip()

		comments.append({'from_name':from_name, 
							'to_name':to_name,
							'text':text})

	return comments

def soup2ids(soup):
	'''
	private function called by $get_comments
	at ids from the usercards, not necessary so far
	'''

	uids = {}
	usercards = soup.findAll('a', attrs={'usercard':re.compile('.*id=\d+.*')})

	for usercard in usercards:
		uname = usercard.text.decode('utf8')
		if uids.has_key(uname):
			continue

		card = usercard.get('usercard')
		m = re.search('id=(\d+)', card)
		uid = m.group(1)
		uids[uname] = uid

	return uids

def add_emoticons_text(html):
	'''
	add title after <img> for each emoticon
	otherwise, soup.text will skip the emoticons
	'''
	return re.sub('<img[^>]*title="(?P<title>[^"]+)"[^>]*type="face"[^>]*>', '\g<title>', html)


def get(uid, mid):
	'''
	shortcut for get_comments
	'''
	return get_comments(uid, mid)

def get_comments(uid, mid, show_result = False):
	url = url_comment(uid, mid)
	response = request(url)

	if response == None:
		return

	try:
		res = json.loads(response)
	except ValueError:
		m = re.search('location.replace\("([^"]+)"\)', response)
		if m == None:
			return
		else:
			print url
			url = m.group(1)
			print url
			return

	comments_count = res['data']['count']

	html = res['data']['html']
	html = add_emoticons_text(html)
	
	soup = BeautifulSoup(html, 'html.parser')

	############ Parse Comments ############
	comments = []
	ids = {}

	cardmore = soup.find('a', attrs={'class':re.compile('.*WB_cardmore.*')})
	if not cardmore:
		'''
		all comments contained in this response
		'''

		ids = soup2ids(soup)
		comments = soup2comments(soup)

	else:
		'''
		comments are shown in severals pages
		more requests for pages required
		'''

		comment_label = soup.find('label', attrs={'for':re.compile('comm_\d+')})
		label_for = comment_label.get('for')
		m = re.match('^comm_(\d+)$', label_for)
		comm_id = m.group(1)

		first_comment = soup.find('div', attrs={'comment_id':re.compile('\d+')})
		max_id = first_comment.get('comment_id')

		#url_comment = cardmore.get('href') + '?type=comment'

		page = 0
		while (len(comments) < comments_count):
			page += 1
			url = url_comment_page(page, comm_id, max_id)
			response = request(url)
			ret = json.loads(response)

			html = ret['data']['html']
			html = add_emoticons_text(html)
			
			soup = BeautifulSoup(html, 'html.parser')
			ids.update(soup2ids(soup))
			comments.extend(soup2comments(soup))

	if show_result:
		#cdata = []
		for c in comments:
			id2 = []
			for name in [c['from_name'], c['to_name']]:
				if name == None:
					id2.append('-1')
				elif not ids.has_key(name):
					id2.append('0')
				else:
					id2.append(ids[name])

			if c['to_name'] == None:
				print '%s: %s'%(c['from_name'], c['text'])
			else:
				print '%s: RE@%s : %s'%(c['from_name'], c['to_name'], c['text'])

			#cdata.append([id2[0], id2[1], c['text']])

	return comments, ids


def search(uid, start_time, key_word):
	url = url_search(uid, start_time, key_word)
	response = request(url)

	if response == None:
		return

	m = re.search(r'<script>parent.FM.view\((.*)\)</script>$', response, re.DOTALL)
	if m == None:
		print 'search: [Error] undefined pattern'
		return None

	json_str = m.group(1)
	
	data  = None
	try:
		data = json.loads(json_str)
	except:
		print 'search: [Error] json failed: %s'%(traceback.format_exc())
		return None

	soup = BeautifulSoup(data['html'], 'html.parser')

	wb_empty = soup.find('div', attrs={'class':'WB_empty'})
	if not wb_empty == None:
		print 'search: [Warning] result not found'
		return None

	wb_text = soup.find('div', attrs={'class':'WB_text'})
	if not wb_text:
		print 'search: [Error] WB_text not found'
		return None

	if not wb_text.text.startswith(key_word):
		print 'search: [Warning] first result mismatches'
		return None

	return wb_text.text


if __name__ == '__main__':
	#uid = '1427605041'
	#mid = '3523152740977956'
	
	uid = '1427605041'
	mid = '3509858479270286'

	ret = get_comments(uid, mid)

	#comment_page(1)
