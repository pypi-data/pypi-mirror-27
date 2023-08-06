import numpy as np
import pandas as pd
import os
import time
import scipy.stats as stats
from numpy.linalg import svd, lstsq
from sklearn.decomposition import PCA
from scipy.stats import linregress, f_oneway
import itertools
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess
from tqdm import tqdm
from sklearn.preprocessing import scale
from sklearn.neighbors import NearestNeighbors
import math
import json
from ctypes import c_int
import pickle
from multiprocess import Pool, current_process, Manager
from functools import partial
from sklearn import preprocessing

class old_fashioned:

    def __init__(self, filename,data_type,pool=None):
        np.random.seed(4574)
        self.data_type = str(data_type)
        if self.data_type == 'p':
            self.raw_data = pd.read_csv(filename,sep='\t').set_index(['Peptide','Protein'])
        if self.data_type == 'r':
            self.raw_data = pd.read_csv(filename,sep='\t').set_index('#')
        if pool != None:
            self.norm_map = pickle.load( open( pool, "rb" ) )
        self.notdone = True

    def pool_normalize(self):
        def pool_normalize(df,dmap):
            newdf = pd.DataFrame(index=df.index)
            for column in df.columns.values:
                newdf[column] = df[column].div(df['pool_'+'%02d' % dmap[column]],axis='index')
            nonpool = [i for i in newdf.columns if 'pool' not in i]
            newdf = newdf[nonpool]
            return newdf

        def qnorm(df):
            ref = pd.concat([df[col].sort_values().reset_index(drop=True) for col in df], axis=1, ignore_index=True).mean(axis=1).values
            for i in range(0,len(df.columns)):
                df = df.sort_values(df.columns[i])
                df[df.columns[i]] = ref
            return df.sort_index()
        if self.data_type == 'r':
            self.data = qnorm(self.raw_data)
            self.scaler = preprocessing.StandardScaler().fit(self.data.values.T)
            self.data = pd.DataFrame(self.scaler.transform(self.data.values.T).T,columns=self.data.columns,index=self.data.index)
        else:
            self.data_pnorm = pool_normalize(self.raw_data,self.norm_map)
            self.data_pnorm = self.data_pnorm.replace([np.inf, -np.inf], np.nan)
            self.data_pnorm = self.data_pnorm.dropna()
            self.data_pnorm = self.data_pnorm.sort_index(axis=1)
            self.data_pnorm = qnorm(self.data_pnorm)
            self.scaler = preprocessing.StandardScaler().fit(self.data_pnorm.values.T)
            self.data = pd.DataFrame(self.scaler.transform(self.data_pnorm.values.T).T,columns=self.data_pnorm.columns,index=self.data_pnorm.index)

    def normalize(self,outname):
        self.old_norm = self.scaler.inverse_transform(self.data.values.T).T
        self.old_norm = pd.DataFrame(self.old_norm,index=self.data.index,columns=self.data.columns)
        if self.data_type == 'p':
            self.old_norm = self.old_norm.groupby(level='Protein').mean()
        self.old_norm.index.names = ['#']
        self.old_norm.to_csv(outname,sep='\t')
