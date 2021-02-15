import numpy as np
import joblib
import warnings
from sqlTool import sqlopen, select_perchange, sqlclose, predtosql

if __name__ == '__main__':
    # pymysql設定資料庫連線設定
    conn, cursor = sqlopen()

    # 把要預測資料取出來
    data = select_perchange(cursor)

    # 轉成 array
    datanp = np.array(data).reshape(1, -1)

    # 讀取訓練好的模型
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)  # 忽略版本警告
        model = joblib.load('StackingClassifier.pkl')

    # 預測模型
    pred = model.predict(datanp)
    result = int(pred[0])
    print(result)
    # 將預測結果存回資料庫
    # predtosql(result, cursor, conn)

    # 資料庫關閉游標及連線
    sqlclose(cursor, conn)