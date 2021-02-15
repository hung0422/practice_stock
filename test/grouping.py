import pandas as pd
import numpy as np
from sklearn.cluster import KMeans



def selfDef(file):
    '''
    自定義分群
    :param file: 欲分群的data檔案名字 type = str
    '''

    data = pd.read_csv('{}.csv'.format(file))
    # print(data)
    # print(len(data))
    list = []

    for i in range(len(data['OpenChange'])):
        change = data.iloc[i,13]
        if change <= 20 and change >= -20:
            a = 0
            list.append(a)
        elif change > 20 :
            a = 1
            list.append(a)
        elif change <-20:
            a = 2
            list.append(a)

    data['selfDef'] = list

    # print(data)

    data.to_csv('./{}.csv'.format(file),index=0,encoding='utf-8')


def skKMeans(file):
    '''
    使用Kmeans分群
    :param file: 欲分群的data檔案名字 type = str
    '''
    data = pd.read_csv('{}.csv'.format(file))
    print(data)
    print(len(data))

    y = [[i] for i in data['OpenChange']]

    # print(y)

    np.random.seed(0)

    # 建立KMeans模型
    model = KMeans(n_clusters=3)
    model.fit(y)

    # 模型自動產生的分類標記
    labels = model.labels_
    print(labels)

    print(len(labels))

    data['kMeans'] = labels

    print(data)

    data.to_csv('./{}.csv'.format(file), index=0, encoding='utf-8')



if __name__ == '__main__':
    selfDef('CleanTest')
    skKMeans('CleanTest')



