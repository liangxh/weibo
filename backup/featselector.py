# -*- coding: utf-8 -*-

from share import *
from datareader import *
from textcleaner import *

import matplotlib.pyplot as plt

import pynlpir
pynlpir.open()

def isspace(text):
	reg = r'^\s*$'
	res = re.match(reg, text)
	if res:
		return True
	return False

def tohist(dlist):
	hist = {}
	for d in dlist:
		if hist.has_key(d):
			hist[d] += 1
		else:
			hist[d] = 1.
	return hist

class FeatSelector:
	def __init__(self):
		self.reader = datareader
		self.textcleaner = textcleaner
		self.emos = self.reader.readEmo()
		self.emoclass, self.emodict = self.reader.readEmoClass()
		self.prefixs = self.reader.readPrefix()
		self.stopwords = self.reader.readStopword()

	def validtoken(self, s):
		 return (not s in self.stopwords) and (not s.startswith('http:')) and (not s.startswith('@'))

	def split_text(self, text):
		text = self.textcleaner.clean(text)

		reg = r'\[([^\[\]\s\d]+)\]'
		pattern = re.compile(reg)
		res = pattern.findall(text)
		emos = list()

		reg1 = r'^([0-9a-zA-Z/]+)?([^0-9a-zA-Z].*)$'
		reg2 = r'^[a-z]+$'

		textlist = []
		for r in res:
			r0 = '[%s]'%(r)
			r = self.textcleaner.clean(r)
			m = re.match(reg1, r)
			flag = False
			if m:
				r = m.group(2)
				flag = True
			else:
				m = re.match(reg2, r)
				if m:
					flag = True
					for p in self.prefixs:
						if r.startswith(p):
							r = r[len(p):len(r)]
							break
			if not flag:
				continue

			if r in self.emos:
				if self.emoclass.has_key(r):				
					loc = text.find(r0)
					textlist.append(text[0:loc])
					text = text[loc + len(r0):len(text)]
					emos.append(r)
				else:
					text = text.replace(r0, ' ')

		textlist.append(text)

		if len(textlist) == 1:
			return []

		emoslist = [{emos[0], }, ]

		validtext = [textlist[0], ]
		for i in range(1, len(emos)):
			t = textlist[i]
			if not isspace(t):
				validtext.append(t)
				emoslist.append({emos[i], })
			else:
				emoslist[-1].add(emos[i])

		if isspace(validtext[0]) and len(validtext) > 1:
			validtext[0] = validtext[1]

		validtext[-1] += ' ' + textlist[-1]

		ret = []
		for i in range(len(emoslist)):
			t = validtext[i]
			tokens = []
			try:
				segs = pynlpir.segment(t, pos_tagging=False)
				for s in segs:
					if self.validtoken(s):
						tokens.append(s)
				for emo in emoslist[i]:
					ret.append((emo, tohist(tokens)))
			except UnicodeDecodeError:
				print t
				None
		return ret

	def split_emo(self, text):
		text = self.textcleaner.clean(text)
		text = re.sub(r'@\S+ ', ' ', text)
		text = re.sub(r'\s+', ' ', text)	

		reg = r'\[([^\[\]\s\d]+)\]'
		pattern = re.compile(reg)
		res = pattern.findall(text)
		emos = list()

		reg1 = r'^([0-9a-zA-Z/]+)?([^0-9a-zA-Z].*)$'
		reg2 = r'^[a-z]+$'

		textlist = []
		for r in res:
			r0 = '[%s]'%(r)
			r = self.textcleaner.clean(r)
			m = re.match(reg1, r)
			flag = False
			if m:
				r = m.group(2)
				flag = True
			else:
				m = re.match(reg2, r)
				if m:
					flag = True
					for p in self.prefixs:
						if r.startswith(p):
							r = r[len(p):len(r)]
							break
			if not flag:
				continue

			if r in self.emos:
				#if self.emoclass.has_key(r):
				if True:				
					loc = text.find(r0)
					textlist.append(text[0:loc])
					text = text[loc + len(r0):len(text)]
					emos.append(r)
				else:
					text = text.replace(r0, ' ')

		textlist.append(text)

		if len(textlist) == 1:
			return []

		emoslist = [{emos[0], }, ]

		validtext = [textlist[0], ]
		for i in range(1, len(emos)):
			t = textlist[i]
			if not isspace(t):
				validtext.append(t)
				emoslist.append({emos[i], })
			else:
				emoslist[-1].add(emos[i])

		if isspace(validtext[0]) and len(validtext) > 1:
			validtext[0] = validtext[1]

		validtext[-1] += ' ' + textlist[-1]

		ret = []
		for i in range(len(emoslist)):
			t = validtext[i]
				

			for emo in emoslist[i]:
				ret.append((emo, t))
		return ret

	def get_feat(self, text):
		tokens = []
		filtered = []
		segs = pynlpir.segment(text, pos_tagging = False)
		for seg in segs:
			if self.validtoken(seg):
				tokens.append(seg)
			else:
				filtered.append(seg)
		return tokens, filtered

	def split_blog(self, blog):
		reg = r'/+@[^:]+:'
		texts = re.sub(reg, '##', blog).split('##')
		return texts

	def print_emo_statics(self):
		hist = {}
		total = 0
		for k, v in self.emoclass.items():
			if hist.has_key(v):
				hist[v] += 1
			else:
				hist[v] = 1

		for k, v in hist.items():
			print '%s : %d'%(k, v)
			total += v
		print '===================='
		print 'Total : %d'%(total)

def testSelector():
	selector = FeatSelector()

	#blog = u'耐心等待//@李易峰全球后援:#李易峰# 啊啊啊啊啊啊啊啊啊！（☜请记得你是官皮☞）李天真你好帅啊！！！！欢迎启程！[心]男神和女神的结合[男孩儿][女孩儿]'
	

	blog = u'[蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛] 至我逝去的三妹   寿命  四十天。'

	texts = selector.split_blog(blog)
	res = selector.split_text(texts[0])
	for emo, tf in res:
		tf_str = []
		for k, v in tf.items():
			tf_str.append('%s:%f'%(k, v))
		
		print '%s: [%s]'%(emo, ', '.join(tf_str))

def testSplitEmo():
	selector = FeatSelector()

	#blog = u'耐心等待//@李易峰全球后援:#李易峰# 啊啊啊啊啊啊啊啊啊！（☜请记得你是官皮☞）李天真你好帅啊！！！！欢迎启程！[心]男神和女神的结合[男孩儿][女孩儿]'

	blog = u'[蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛][蜡烛] 至我逝去的三妹 [蜡烛][扭動][开心] 寿命 四十天。'

	texts = selector.split_blog(blog)
	ret = selector.split_emo(texts[0])
	for emo, t in ret:
		print '%s: %s'%(emo, t)

def saveBlogFeature():
	selector = FeatSelector()
	lines = selector.reader.readText()
	docs = []
	print len(lines)
	for d in lines:
		docs.extend(selector.split_blog(d))
	print len(docs)
	
	db = []

	total = len(docs)
	count = 0
	for d in docs:
		d = d.replace('#', ' ').replace('|', ' ')
		texts = selector.split_blog(d)
		for text in texts:
			res = selector.split_text(text)
			db.extend(res)
		count += 1
		if (count % 500 == 0):
			print '%d / %d'%(count, total)

	print len(db)

	fobj = open(FILE_FEAT, 'w')
	for emo, tf in db:
		item = {'emo':emo, 'tf':tf}
		fobj.write('%s\n'%(json.dumps(item)))
	fobj.close()

def checkBlogEmo():
	selector = FeatSelector()
	lines = selector.reader.readText()
	docs = []
	print len(lines)
	for d in lines:
		docs.extend(selector.split_blog(d))
	print len(docs)

	emocount = []

	total = len(docs)
	count = 0
	for d in docs:
		d = d.replace('#', ' ').replace('|', ' ')
		texts = selector.split_blog(d)
		for text in texts:
			res = selector.split_text(text)
			emocount.append(len(res))
		count += 1
		if (count % 500 == 0):
			print '%d / %d'%(count, total)

	emocount = tohist(emocount)
	for k, v in emocount.items():
		print k, v

def sqr(x):
	return x * x

def testChi():
	reader = DataReader()
	feats = reader.readFeat()
	emoclass, emodict = reader.readEmoClass()

	emos = emodict.keys()

	dfs = {}
	emocount = {}

	for emo in emos:
		dfs[emo] = {}
		emocount[emo] = 0.

	tokens = set()

	for feat in feats:
		femo = feat['emo']
		if not emoclass.has_key(femo):
			continue

		emo = emoclass[feat['emo']]
		df = dfs[emo]
		emocount[emo] += 1

		tf = feat['tf']
		for k, v in tf.items():
			tokens.add(k)
			if df.has_key(k):
				df[k] += 1
			else:
				df[k] = 1.

	N = sum(emocount.values())

	print len(tokens)

	maxchi = -1
	minchi = 1000000000000

	tchis = {}

	for t in tokens:
		tfs = {}
		for k, v in dfs.items():
			if v.has_key(t):
				tfs[k] = v[t]
			else:
				tfs[k] = 0.
		chis = {}
		tfs_sum = sum(tfs.values())

		for k, v in tfs.items():
			a = v
			c = emocount[k] - a
			
			b = tfs_sum - a
			d = (N - emocount[k]) - b
			chi = sqr(a * d - c * b) /((a + c) * (b + d) * (a + b) * (c + d))
			chis[k] = chi

		tchis[t] = chis

	cchis = {}
	for emo in emos:
		cchis[emo] = {}

	for t, chis in tchis.items():
		for k, v in chis.items():
			cchis[k][t] = v

	seeds = {}
	for emo in emos:
		seeds[emo] = set()
	
	num = 600
	for k, v in cchis.items():
		v = sorted(v.items(), key = lambda k:k[1], reverse = True)
		for i in range(num):
			seeds[k].add(v[i][0])

	return emos, tchis, seeds

def getSeed():
	emos, tchis, seeds = testChi()
	for k, v in seeds.items():
		print '> %s: %d'%(k, len(v))
		print ', '.join(v)

def saveLstmInput():
	selector = FeatSelector()
	db = selector.reader.readText()
	collection = {}
	for d in db:
		texts = selector.split_blog(d)
		for text in texts:
			ret = selector.split_emo(text)
			for emo, t in ret:
				if collection.has_key(emo):
					collection[emo].add(t)
				else:
					collection[emo] = set([t, ])
	
	filtered = {}
	for k, v in collection.items():
		if len(v) > 1000:
			filtered[k] = list(v)

	fobj = open(FILE_NN_INPUT, 'w')
	fobj.write(json.dumps(filtered))
	fobj.close()

if __name__ == '__main__':
	None
	saveLstmInput()

	#testSplitEmo()
	#testSelector()
	#saveBlogFeature()
	#checkBlogEmo()
	#testFeature()
	#selector.print_emo_statics()
	
	#getSeed()

