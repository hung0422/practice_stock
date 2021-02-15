import pandas as pd
import random

data = pd.read_csv(r'Cleanfinal1.csv')

# print(data)

#自定義項目為1的選出來
pd2 = data[data['selfDef'] == 1]

# print(pd2)

#隨機複製150份樣本
pdrandom = pd2.sample(150)

# print(pdrandom)

#加入data
data3 = data.append(pdrandom,ignore_index=False )

print(data3)

#儲存檔案
data3.to_csv('Cleanfinal1.csv', index=False)