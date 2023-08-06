import pandasfiles as pf
import numpy as np







if __name__ == '__main__':
    import tushare as ts
    dis = pf.Distribution(chunk=2,mode='w',auto=True)
    dis.start()
    stock_data = ts.get_stock_basics()
    for i in stock_data.index.tolist()[8:30]:
        name = 'st'+i
        zz = ts.get_k_data(i)
        dis.write(name,zz)
    dis.end()
    df = dis.get_data('st002161')
    print(df)
