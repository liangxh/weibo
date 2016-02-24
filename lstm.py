#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.23
Description: Interface for Lstm
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from utils import lstmtool
import theano
import numpy as np
from utils.logger import Logger

logger = Logger()

class LstmClassifier:
	def __init__(self):
		pass

	def log(self, func_name, debug_type, )

	########################## Classification ###################################
	def load(self, 
		ydim, n_words,
		dim_proj = 128,
		encoder = 'lstm',
		use_dropout = True,
		fname_model = 'lstm_mode.npz', 
	):
		model_options = locals().copy()
		params = lstmtool.init_tparams(params)
		
		lstmtool.load_params(fname_model, params)	
		tparams = lstmtool.init_tparams(params)

		use_noise, x, mask, y, f_pred_prob, f_pred, cost = build_model(tparams, model_options)

		self.f_pred = f_pred
		self.f_pred_prob = f_pred_prob

	def classify_batch(self, seqs):
		x, x_mask = self.prepare_x(seqs)
		ps = self.f_pred(x, x_mask)
		pds = self.f_pred_prob(x, x_mask)

		return ps, pds

	def classify(self, seqs, batch_size = 64):
		if not instance(seqs[0], list):
			seqs = [seqs, ]
			preds, pred_probs = self.classify_batch(seqs)

			logger.warning('not examined yet, please check')
			return preds[0], pred_probs[0]
		else:
			kf = lstmutil.get_minibatcches_idx(len(seqs), batch_size)
		
			preds = []
			pred_probs = []

			for _, idx in kf:
				ps, pds = self.classify_batch([seqs[i] for i in idx])	
				preds.extend(ps)
				pred_probs.extend(pds)

			return preds, pred_probs

	######################## Training ##########################################
	def prepare_x(self, seqs):
		'''
		create two 2D-Arrays (seqs and mask)
		'''
		lengths = [len(s) for s in seqs]

		n_samples = len(seqs)
		maxlen = np.max(lengths)

		x = np.zeros((maxlen, n_samples))	#.astype('int64')
		x_mask = np.zeros(maxlen, n_samples)	#.astype(theano.config.floatX)

		for idx, s in enumerate(seqs):
			x[:lengths[idx], idx] = s
			x_mask[:lengths[idx], idx] = 1.
		
		return x, x_mask
	
	def train(self,
		dataset,

		# model params		
		ydim, n_words,
		dim_proj = 128,
		encoder = 'lstm',
		use_dropout = True,
		reload_model = False,
		fname_model = None,
		
		# training params
		validFreq = None, # 1000
		saveFreq = None, #1000
		patience = 10,
		max_epochs = 5000,
		decay_c = 0.,
		lrate = 0.0001,
		batch_size = 16,
		valid_batch_size = 64,
		optimizer = lstmtool.adadelta,
		noise_std = 0., 

		# debug params
		dispFreq = 10,
	):

		train, valid, test = dataset

		# building model
		logger.info('building model...')

		model_options = locals().copy()
		params = lstmtool.init_params(model_options)

		if reload_model:
			if os.path.exists(fname_model):
				lstmtool.load_params(fname_model, params):
			else:
				logger.warning('model %s not found'%(fname_model))
				return None
		
		tparams = lstmtool.init_tparams(params)
		use_noise, x, mask, y, f_pred_prob, f_pred, cost = build_model(tparams, model_options)

		# preparing functions for training
		logger.info('preparing functions')

		if decay_c > 0.:
			decay_c = theano.shared(lstmtool.numpy_floatX(decay_c), name='decay_c')
			cost += (tparams['U'] ** 2).sum() * decay_c
	
		f_cost = theano.function([x, mask, y], cost, name = 'f_cost')
		
		grads = tensor.grad(cost, wrt = tparams.values())
		f_grad = theano.function([x, mask, y], grads, name = 'f_grads')

		lr = tensor.scalar(name = 'lr')
		f_grad_shared, f_update = optimizer(lr, tparams, grads, x, mask, y, cost)

		kf_valid = lstmtool.get_minibatches_idx(len(valid[0]), valid_batch_size)
		kf_test = lstmtool.get_minibatches_idx(len(test[0]), valid_batch_size)

		if validFreq == None:
			validFreq = len(train[0]) / batch_size
		
		if saveFreq == None:
			saveFreq = len(train[0]) / batch_size
		
		history_errs = []
		best_p = None
		bad_count = 0

		uidx = 0       # number of update done
		estop = False  # early stop

		# training
		logger.info('start training...')

		try:
			for eidx in xrange(max_epochs):
				n_samples = 0
				
				kf = lstmtool.get_minibatches_idx(len(train[0]), batch_size, shuffle = True)
				
				for _, train_index in df:
					uidx += 1
					use_noise_set_value(1.)

					x = [train[1][t] for t in train_index]
					y = [train[0][t] for t in train_index]

					x, mask = self.prepared
if __name__ == '__main__':
	pass
