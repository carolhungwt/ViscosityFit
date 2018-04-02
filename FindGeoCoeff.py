#!/usr/bin/env python
#FindGeoCoeff.py

class NiDisc(object):
	def __init__(self,d,l):
		self.l = float(l)
		self.d = float(d)

	@property
	def Dcol(self):
		taumat = np.array([[5,1],[2,4]])
		taucol = np.array([[1./self.taub],[1./self.tauc]])
		invtaumat = np.linalg.inv(taumat)
		Dcol = np.matmul(invtaumat,taucol)
		return Dcol

	@property
	def Dperp(self):
		return self.Dcol[0][0]

	@property 
	def Dpara(self):
		return self.Dcol[1][0]

	@property
	def taua(self):
		tauadivtau0 = 1.18+0.1744(np.log(self.p)+0.2877)**2-0.2417*(np.log(self.p+0.2877))**3-0.03882*(np.log(self.p)-0.2877)**4
		return tauadivtau0

	@property
	def taub(self):
		taub = 1.183+0.2902*(np.log(self.p))+0.4406*(np.log(self.p))**2-0.0585*(np.log(self.p))**3-0.009544*(np.log(self.p))**4
		return taub

	@property
	def tauc(self):
		tauc = 0.9833+0.06532/(np.log(self.p))+0.05168/(np.log(self.p)**2)-0.003234/(np.log(self.p)**3)
		return tauc

	@property
	def p(self):
		p = self.l/self.d
		return p

import os, argparse
import numpy as np
if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--diameter',help='diameter of the disc, in micrometer', default=40, type=float)
	parser.add_argument('-l','--length', help='height of the disc, in Angstrum', default=3000, type=float)
	args = parser.parse_args()

	a = NiDisc(args.diameter,args.length)
	print 1/a.taub
	print 1/a.tauc
	print a.Dpara
