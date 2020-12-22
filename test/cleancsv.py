import pandas as pd

def cleancsv(file):
    # 讀取原始資料的'日期'欄位
    df = pd.read_csv('test.csv')
    df2 = df['日期']

    # 將日期取出來
    dflist =df2.values.tolist()
    dflist2 = [i for i in dflist]
    # print(dflist2)

    # 變成字典 key:日期, value:null
    alldict = {}
    for i in dflist2:
        alldict[i] = 'null'
    # print(alldict)

    # 讀取目標資料的'日期', 'Close'欄位
    dff = pd.read_csv('{}.csv'.format(file))
    dff2 = dff[['Date','Close']]
    # 把值取出來
    dfflist = dff2.values.tolist()
    # print(dfflist)

    # 和字典的原始資料日期比較,如果有值就覆蓋過去
    for i in dfflist:
        if i[0] in alldict:
            alldict[i[0]] = round(i[1],2)
    # print(alldict)

    # 把value取出來
    alllist = []
    for i in alldict:
        alllist.append(alldict[i])
    # print(alllist)

    # 合併原始資料並存檔
    df['{}'.format(file)] = alllist
    # print(df)
    df.to_csv('test.csv', index=False)

cleancsv('FCHI')