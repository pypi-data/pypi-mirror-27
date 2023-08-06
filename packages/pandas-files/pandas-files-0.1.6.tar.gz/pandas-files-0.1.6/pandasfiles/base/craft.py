# coding:utf-8
import pandas as pd
import joblib
from pandasfiles.utils.tools import find_path


class Craft:

    def __init__(self,mode,store_path='',store_name='',ktype='hdfs'):
        self.mode = mode
        self.ktype = ktype
        if '.h5' in str(store_name):
            self.s_name = store_name
        else:
            raise ValueError('store_name must named xxx.h5,please check it.')

        if store_path == '':
            self.s_path = find_path('tmp')
        else:
            self.s_path = store_path

    def start(self):
        if self.ktype == 'hdfs':
            self.hdfs = pd.HDFStore(self.s_path + self.s_name, mode=self.mode, complevel=9, complib='blosc')
        elif self.ktype == 'joblib':
            if self.mode == 'w':
                self.job = {}
            elif self.mode == 'a':
                self.job =joblib.load(self.s_path+self.s_name)
            elif self.mode in ['r','r+']:
                self.job =joblib.load(self.s_path+self.s_name)

        else:
            raise ValueError("ktype only can be 'hdfs' or 'joblib'.")


    def read(self,key):
        if self.ktype == 'hdfs':
            self.start()
            resp = self.hdfs[key]
            self.end()
            return resp
        elif self.ktype == 'joblib':
            resp = joblib.load(self.s_path+self.s_name)[key]
            return resp

    def _built_in_read(self,key):
        if self.ktype == 'hdfs':
            resp = self.hdfs[key]
            return resp
        elif self.ktype == 'joblib':
            resp = joblib.load(self.s_path+self.s_name)[key]
            return resp



    def write(self,key,value):
        if self.mode in ['w','a']:
            if self.ktype == 'hdfs':
                if '/'+key in self.hdfs.keys():
                    self.append(key,value,reset_index=False)
                else:
                    self.hdfs[key] = value
                return self.hdfs[key]
            elif self.ktype == 'joblib':
                self.job[key] = [value]
                return self.job[key]
        elif self.mode in ['r','r+']:
            raise ValueError("the mode is 'r',you only can read.")


    def append(self,key,value,reset_index=True):
        if self.mode in ['w','a']:
            if self.ktype == 'hdfs':
                self.hdfs[key] = self.hdfs[key].append(value)
                if reset_index == True : self.hdfs[key] = self.hdfs[key].reset_index(drop=True)
                return self.hdfs[key]
            elif self.ktype == 'joblib':
                self.job[key].append(value)
                return self.job[key]
        elif self.mode in ['r','r+']:
            raise ValueError("the mode is 'r',you only can read.")

    def end(self):
        if self.ktype == 'hdfs':
            self.hdfs.close()
        elif self.ktype == 'joblib':
            joblib.dump(self.job,self.s_path+self.s_name)


