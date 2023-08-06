#!/usr/bin/python
# -*- coding: utf-8 -*-

# WOE & IV值
'''
iv

calculate woe and iv.

'''

import numpy as np
import pandas as pd

def table(data,target,columns):
	sample=pd.DataFrame(index=sorted(data[columns].unique()))
	# count
	sample['n0']=(data[target]==0).groupby(data[columns]).sum()
	sample['n1']=(data[target]==1).groupby(data[columns]).sum()
	sample['n']=sample['n0']+sample['n1']
	sample.loc['sum',:]=sample.sum()
	sample['p0']=sample['n0']/sample['n0']['sum']
	sample['p1']=sample['n1']/sample['n1']['sum']
	sample['woe']=np.log(sample['p1']/sample['p0'])
	sample['iv']=(sample['p1']-sample['p0'])*np.log(sample['p1']/sample['p0'])
	sample.loc['sum','iv']=sample['iv'].sum()
	return sample

if __name__ == '__main__':
	print('你好!')

# done