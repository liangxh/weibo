#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.03.08
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import cPickle
import matplotlib.pyplot as plt


from utils import progbar

def analyse_result(ys, pred_probs):
	n_test = len(ys)	
	n_dim = len(pred_probs[0])
	hit = [0 for i in range(n_dim)]

	for y, probs in zip(ys, pred_probs):
		eid_prob = sorted(enumerate(probs), key = lambda k:-k[1])

		for i, item in enumerate(eid_prob):
			eid, progs = item
			if y == eid:
				hit[i] += 1

	for i in range(1, n_dim):
		hit[i] += hit[i - 1]
	
	acc = [float(hi) / n_test for hi in hit]

	plt.figure()
	plt.xlabel('Rank N')
	plt.ylabel('Precision')
	plt.plot(range(1, n_dim + 1), acc)

	rand_x = range(1, n_dim + 1)
	rand_y = [float(xi) / n_dim for xi in rand_x]
	plt.plot(rand_x, rand_y, '--r') 

	plt.savefig('precision.png')

def test():
	import cPickle
	
	'''
	import unidatica
	from const import N_EMO

	n_emo = N_EMO
	dataset = unidatica.load(n_emo)
	preds, pred_probs = cPickle.load(open('output/pred_result.pkl', 'r'))
	test_y = dataset[2][1]

	cPickle.dump((test_y, pred_probs), open('output/lstm_result.pkl', 'w'))
	'''
	test_y, pred_probs = cPickle.load(open('output/lstm_result.pkl', 'r'))
	
	analyse_result(test_y, pred_probs)

if __name__ == '__main__':
	test()
