import pandasfiles as pf
import numpy as np







if __name__ == '__main__':
    import tushare as ts
    dis = pf.Distribution(chunk=2,mode='a',auto=True,check_repeat_columns='date')
    dis.start()
    stock_data = ['600115','000400','600225']
    for i in stock_data:
        name = 'st'+i
        zz = ts.get_k_data(i,start='2017-01-01',end='2017-10-03')
        dis.write(name,zz)
    dis.end()
    # df = dis.get_data('st002505')
    # print(df)
