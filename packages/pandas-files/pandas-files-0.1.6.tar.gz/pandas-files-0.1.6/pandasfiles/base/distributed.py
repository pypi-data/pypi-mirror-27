# coding:utf-8
import os
import re
import joblib
from pandasfiles.base.craft import Craft
from pandasfiles.base.template import STORE_NAME,PARTITION_VARIABLE,FILE_KEYS_LIST,INDEX_FILE
from pandasfiles.utils.lylogger import tolog



class Distribution:


    def __init__(self,partition_name,chunk,mode,ktype,index_path,sub_store,log_file_path,silent,check_repeat_columns):

        self.__partition_name = partition_name
        self.__chunk = chunk
        self.__mode = mode
        self.__index_path = index_path
        self.__sub_store = sub_store
        self.__ktype = ktype
        self.__logger = tolog(operate_name='distributed', log_file_path=log_file_path,silent=silent)
        self.__check_repeat_columns = check_repeat_columns

        if mode in ['a','r','r+']:
            try:
                json = joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))
                self.__RE_CHUNKED_INDEXS = json['reindex']
                self.__CHUNKED_INDEXS = json['index']
                self.__KEYS = json['keys']
                self.__partitions = json['partitions']
                self.__FILE_POSITIONS = json['position']
            except:
                raise IOError('Please set current mode if you have operation before.')
        elif mode == 'w':
            self.__RE_CHUNKED_INDEXS = {}
            self.__CHUNKED_INDEXS = {}
            self.__KEYS = []
            self.__partitions = []
            self.__FILE_POSITIONS = {}

        else:
            raise ValueError("mode only can set 'a' , 'w' ,'r' and 'r+'.")

    # 计算对应子结点下的keys数量
    def _check_keys_count(self,is_sorted=True,mode='w'):
        dCounts = {}
        if mode == 'w':
            for i in range(0,self.__chunk):
                s_name = STORE_NAME.format(self.__partition_name,i)
                if s_name in self.__RE_CHUNKED_INDEXS.keys():
                    dCounts[s_name] = len(self.__RE_CHUNKED_INDEXS[s_name])
                else:
                    dCounts[s_name] = 0
        elif mode in ['a','r','r+']:
            dCounts = {k:len(v) for k,v in self.__RE_CHUNKED_INDEXS.items()}

        if is_sorted == False:
            return dCounts
        else:
            return sorted(dCounts.items(), key=lambda x: x[1], reverse=True)


    # 文件名对应索引
    def _get_file_index(self,string):
        return int(re.findall("\[(.*?)\]",string)[0])


    def start(self):
        if self.__mode == 'w':
            for chunk_i in  range(0,self.__chunk):
                s_name = STORE_NAME.format(self.__partition_name,chunk_i)
                globals()[PARTITION_VARIABLE.format(chunk_i)] = Craft(mode='w',
                                                                      store_path=self.__sub_store[chunk_i],
                                                                      store_name=s_name,
                                                                      ktype=self.__ktype)
                globals()[FILE_KEYS_LIST.format(chunk_i)] =[]
                globals()[PARTITION_VARIABLE.format(chunk_i)].start()
                # 位置信息
                self.__FILE_POSITIONS[s_name] = self.__sub_store[chunk_i]

        elif self.__mode in ['a','r','r+']:
            for s_name in self.__partitions:
                chunk_i = self._get_file_index(s_name)
                globals()[PARTITION_VARIABLE.format(chunk_i)] = Craft(mode=self.__mode,
                                                                      store_path=self.__sub_store[chunk_i],
                                                                      store_name=s_name,
                                                                      ktype=self.__ktype)
                globals()[FILE_KEYS_LIST.format(chunk_i)] = self.__RE_CHUNKED_INDEXS[s_name]
                globals()[PARTITION_VARIABLE.format(chunk_i)].start()
                # 位置信息
                self.__FILE_POSITIONS[s_name] = self.__sub_store[chunk_i]



    def write(self,key,value):

        if self.__mode == 'w':

            keyCounts = self._check_keys_count(mode='w')
            fileIndex = self._get_file_index(keyCounts[-1][0])
            globals()[PARTITION_VARIABLE.format(fileIndex)].write(key,value)
            globals()[FILE_KEYS_LIST.format(fileIndex)].append(key)
            self.__KEYS.append(key)
            s_name = STORE_NAME.format(self.__partition_name, fileIndex)
            self.__RE_CHUNKED_INDEXS[s_name] = globals()[FILE_KEYS_LIST.format(fileIndex)]

            if len(value) != 0 : self.__logger.printf_debug('%s succeed in %s.'%(key,s_name))
            else: self.__logger.printf_debug('%s is empty.'%key)

        elif self.__mode == 'a':

            if key in self.__KEYS:
                s_name = self.__CHUNKED_INDEXS[key]
                fileIndex = self._get_file_index(s_name)

                # add check_repeat_columns
                if self.__check_repeat_columns != None and value.empty is False :
                    check = globals()[PARTITION_VARIABLE.format(fileIndex)]._built_in_read(key)
                    if check.empty is False:
                        if  self.__check_repeat_columns not in check.columns and self.__check_repeat_columns not in value.columns:
                            self.end()
                            raise ValueError('if you want to check repeat values,please write current column but not "{}" and mode must be "hdfs".'.format(self.__check_repeat_columns))
                        else:
                            if len(set(check[self.__check_repeat_columns])&set(value[self.__check_repeat_columns])) !=0:
                                self.__logger.printf_debug("the new value is repeated by {}.".format(key))
                            else:
                                globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)
                    else:
                        globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)

                else:
                    globals()[PARTITION_VARIABLE.format(fileIndex)].append(key, value)
            else:
                keyCounts = self._check_keys_count(mode='a')
                fileIndex = self._get_file_index(keyCounts[-1][0])
                globals()[PARTITION_VARIABLE.format(fileIndex)].write(key,value)
                globals()[FILE_KEYS_LIST.format(fileIndex)].append(key)
                self.__KEYS.append(key)
                s_name = STORE_NAME.format(self.__partition_name, fileIndex)
                self.__RE_CHUNKED_INDEXS[s_name] = globals()[FILE_KEYS_LIST.format(fileIndex)]

            if len(value) != 0 : self.__logger.printf_debug('%s succeed in %s.'%(key,s_name))
            else: self.__logger.printf_debug('%s is empty.'%key)

        elif self.__mode in ['r','r+']:
            self.end()
            raise ValueError("the mode is 'r',you only can read.")


    def end(self):
        if self.__mode == 'w':
            for chunk_i in  range(0,self.__chunk):
                globals()[PARTITION_VARIABLE.format(chunk_i)].end()
        elif self.__mode in ['a','r','r+']:
            for s_name in self.__partitions:
                chunk_i = self._get_file_index(s_name)
                globals()[PARTITION_VARIABLE.format(chunk_i)].end()


        self.__CHUNKED_INDEXS = {}
        for k,v in self.__RE_CHUNKED_INDEXS.items():
            for j in v:
                self.__CHUNKED_INDEXS[j] = k
        self.__partitions = list(self.__RE_CHUNKED_INDEXS.keys())
        sets = {
            'keys': self.__KEYS,
            'index': self.__CHUNKED_INDEXS,
            'reindex': self.__RE_CHUNKED_INDEXS,
            'partitions': self.__partitions,
            'position':self.__FILE_POSITIONS
        }
        joblib.dump(sets, self.__index_path+ INDEX_FILE.format(self.__partition_name))

    def get_data(self,key):
        json = joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))
        key_to_file = json['index'][key]
        craft = Craft(mode='r+',store_path=json['position'][key_to_file],store_name=key_to_file,ktype=self.__ktype)
        resp = craft.read(key)
        return resp

    @property
    def keys(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['keys']

    @property
    def index(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['index']

    @property
    def reindex(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['reindex']

    @property
    def partitions(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['partitions']

    @property
    def positions(self):
        return joblib.load(self.__index_path+ INDEX_FILE.format(self.__partition_name))['position']









