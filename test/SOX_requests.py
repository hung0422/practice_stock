import requests, time
from bs4 import BeautifulSoup

ss = requests.session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
# 網址
url = 'https://finance.yahoo.com/quote/%5ESOX/history?p=%5ESOX'
# 爬蟲設定
res =ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

# 名稱
title = soup.select('div[class="D(ib)"]')[0].text
content = soup.select('tr[class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')[0]
# 日期
Date_before = content.select('td[class="Py(10px) Ta(start) Pend(10px)"]')[0].text
# 轉換時間格式
Date_change = time.strptime(Date_before, "%b %d, %Y")
Date = time.strftime("%Y-%m-%d", Date_change)
# 開盤
Open = content.select('td[class="Py(10px) Pstart(10px)"]')[0].text
# 最高
High = content.select('td[class="Py(10px) Pstart(10px)"]')[1].text
# 最低
Low = content.select('td[class="Py(10px) Pstart(10px)"]')[2].text
# 收盤
Close = content.select('td[class="Py(10px) Pstart(10px)"]')[3].text
# 調整後收盤
Adj_Close = content.select('td[class="Py(10px) Pstart(10px)"]')[4].text

print('title:',title)
print('Date:',Date)
print('Open:',Open)
print('High:',High)
print('Low:',Low)
print('Close:',Close)
print('Adj_Close:',Adj_Close)