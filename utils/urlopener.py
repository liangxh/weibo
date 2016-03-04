#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.03.01
Description: A wrapper for urllib, cookie may be added later
'''

import urllib
import urllib2
import socket
import cookielib

TIMEOUT = 10
import StringIO, gzip


COOKIE = "SINAGLOBAL=1540155493936.2783.1437873991846; ULV=1456794881815:27:1:3:6736351011202.016.1456794881809:1456707385887; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF8iBEe7Vbs5Dm_iUTSeI9Y5JpX5K2t; SUHB=0V51XKG4HDXPCk; UOR=,,login.sina.com.cn; __gads=ID=1a8f779f4b7dca3b:T=1438945266:S=ALNI_MZd8HiJR9pQ4NlZ6BpXXFPL5mRK2g; _ga=GA1.2.1558033104.1449374459; SUB=_2A2570XeCDeTxGeNO41UX8ifIyjWIHXVYp-5KrDV8PUJbuNAPLU_fkW9LHesQkXvejbWmODzHgRcsAxxayVSiAA..; myuid=5087629419; un=axit9ocw63hn@163.com; login_sid_t=898ecdca2e2ba656704bbb8a9658da68; _s_tentry=weibo.com; Apache=6736351011202.016.1456794881809; SUS=SID-5087629419-1456801746-XD-x9e8v-5da2d753380b47e6f3664c48ec8ad02e; SUE=es%3D34c1d412f14326d025e0234bb8b056dd%26ev%3Dv1%26es2%3Dcca209e884c4e90d4172e6c3abbfe147%26rs0%3DXeqPSD1Tc5FcWoI6PVrY4Ha%252F22Bkwjm4Q5ICguTECUDxardzj7fuARaUl%252BBUbL6kq%252B%252FmpkMnHuRgF8yeIEKS3Zx9wVAs6Zv9oi3ILVuwOlS%252F9Q30Swe%252FF6BBUIP15jDyxKIjZJPTIh4cTAr%252FoVCiEnreBTNLIKTUgwnubHGQU0k%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1456801746%26et%3D1456888146%26d%3Dc909%26i%3Dd02e%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D5087629419%26name%3Daxit9ocw63hn%2540163.com%26nick%3DL_%25E6%2598%25AF%25E6%2588%2591%25E7%259A%2584%25E6%25B5%25B7%25E4%25B8%259C%26fmp%3D%26lcp%3D2015-09-08%252017%253A55%253A20; SSOLoginState=1456801746; wvr=6"

class UrlOpener:
	__DEFAULT_TIMEOUT = 10

	def __init__(self):
		self.timeout = self.__DEFAULT_TIMEOUT
		self.header = UrlOpener.default_header()
		self.opener = UrlOpener.build_opener()

	@classmethod
	def default_header(self):
		return {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch', 
			'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
			'Connection':'keep-alive',
			'Cookie':'',
			}

	@classmethod
	def build_opener(self):
		null_proxy_handler = urllib2.ProxyHandler({})
		opener = urllib2.build_opener(null_proxy_handler)

		return opener

	@classmethod
	def ungzip(self, data):
		'''
		decompress the response package
		'''
		compressedstream = StringIO.StringIO(data)  
		gziper = gzip.GzipFile(fileobj = compressedstream)    
		content = gziper.read()

		return content

	def set_timeout(self, timeout):
		self.timeout = timeout

	def set_cookie(self, cookie):
		self.header['Cookie'] = cookie

	def clear_cookie(self):
		self.header['Cookie'] =  ''

	def empty_cookie(self):
		return self.header['Cookie'] == ''

	def urlopen(self, url, data = None):
		req = urllib2.Request(url, headers = self.header)

		try:
			resp = self.opener.open(req, data = data, timeout = self.timeout)
			content = resp.read()

			is_gzip = resp.headers.dict.get('content-encoding') == 'gzip'
			if is_gzip:
				content = UrlOpener.ungzip(content)

			return content
		except urllib2.URLError, e:
			print e.reason
			return None
		except urllib2.HTTPError, e:
			print '[ERRNO %d] %s'%(e.code, e.reason)
			return None
		except socket.timeout, e:
			print '[Timeout] %s'%(e.reason)
			return None

def test():
	opener = UrlOpener()
	content = opener.urlopen('http://www.baidu.com/')
	print content

if __name__ == '__main__':
	test()
	
