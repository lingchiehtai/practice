# -*- coding: utf-8 -*-
"""
@author: Linda Tai
"""

#爬取臺灣銀行牌告匯率，並畫出歷史趨勢圖   

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import datetime
import matplotlib.pyplot as plt


date = datetime.date.today()
#print(date)
dd=str(date).split("-")
dd=dd[1]+'/'+dd[2]

url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
res = requests.get(url)                          # 取得網頁內容
soup = BeautifulSoup(res.text, "html.parser")    # 轉換內容
datas = soup.find_all('tr') 

list1 = []
for i in datas:
    try:
        curr=i.find('div', class_='hidden-phone print_show xrt-cur-indent').get_text().strip()
        cashBuy=i.find_all('td', class_='rate-content-cash text-right print_hide')[0].get_text()
        cashSell=i.find_all('td', class_='rate-content-cash text-right print_hide')[1].get_text()
    
        #print(f'{curr}|現金買入:{cashBuy}|現金賣出:{cashSell}')
        list1.append([curr, float(cashBuy), float(cashSell)])
        
    except:
        pass

df1 = pd.DataFrame(list1)
USD_buy = df1.iloc[0,1]
USD_sell = df1.iloc[0,2]
JPY_buy = df1.iloc[7,1]
JPY_sell = df1.iloc[7,2]
EUR_buy = df1.iloc[13,1]
EUR_sell = df1.iloc[13,2]

with open('exchange_rate_history.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    #writer.writerow(['date', 'USDbuy', 'USDsell', 'JPYbuy', 'JPYsell', 'EURbuy', 'EURsell'])
    writer.writerow([dd, USD_buy, USD_sell, JPY_buy, JPY_sell, EUR_buy, EUR_sell])


#----------------------------------------
# 讀取 csv 檔案內容
x1=[]
y_USDbuy, y_USDsell = [], []
y_JPYbuy, y_JPYsell = [], []
y_EURbuy, y_EURsell = [], []
with open('exchange_rate_history.csv', newline='', encoding='utf-8') as csvfile: 
    rows = csv.reader(csvfile)   
    for row in rows:
        if rows.line_num == 1: #忽略第一列的title
            continue
        x1.append(row[0])
        y_USDbuy.append(float(row[1]))
        y_USDsell.append(float(row[2]))
        y_JPYbuy.append(float(row[3]))
        y_JPYsell.append(float(row[4]))
        y_EURbuy.append(float(row[5]))
        y_EURsell.append(float(row[6]))

#plot
fig1  = plt.figure(figsize=(10,20), dpi=150)

plt.subplot(3,1,1)
#plt.axes([0.15, 0.15, 0.75, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, y_USDbuy, color = 'red', label='Buying', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x1, y_USDsell, color = 'blue', label='Selling', marker='o', markersize=12, linestyle = '--', linewidth=3)
stride = 5
plt.legend(loc = 'best')
plt.xticks(ticks=x1[::stride], labels=x1[::stride], fontsize=14, rotation=20)
plt.yticks(fontsize=14, rotation=0)
plt.grid(True)
plt.xlabel('Date', size=20) 
plt.ylabel('Exchange Rate', size=20) 
plt.title('Cash Rate (USD)', size=18) 
plt.tight_layout() #子圖表保持合適的間距
#plt.savefig('exchange_rate_USD.png') 

#plot
#fig2  = plt.figure(figsize=(10,6), dpi=120)

plt.subplot(3,1,2)
#plt.axes([0.15, 0.15, 0.75, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, y_JPYbuy, color = 'red', label='Buying', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x1, y_JPYsell, color = 'blue', label='Selling', marker='o', markersize=12, linestyle = '--', linewidth=3)
stride = 5
plt.legend(loc = 'best')
plt.xticks(ticks=x1[::stride], labels=x1[::stride], fontsize=14, rotation=20)
plt.yticks(fontsize=14, rotation=0)
plt.grid(True)
plt.xlabel('Date', size=20) 
plt.ylabel('Exchange Rate', size=20) 
plt.title('Cash Rate (JPY)', size=18) 
plt.tight_layout()
#plt.savefig('exchange_rate_JPY.png') 

#plot
#fig3  = plt.figure(figsize=(10,6), dpi=120)

plt.subplot(3,1,3)
#plt.axes([0.15, 0.15, 0.75, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, y_EURbuy, color = 'red', label='Buying', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x1, y_EURsell, color = 'blue', label='Selling', marker='o', markersize=12, linestyle = '--', linewidth=3)
stride = 5
plt.legend(loc = 'best')
plt.xticks(ticks=x1[::stride], labels=x1[::stride], fontsize=14, rotation=20)
plt.yticks(fontsize=14, rotation=0)
plt.grid(True)
plt.xlabel('Date', size=20) 
plt.ylabel('Exchange Rate', size=20) 
plt.title('Cash Rate (EUR)', size=18) 
plt.tight_layout()

plt.savefig('exchange_rate_USD_JPY_EUR.png') 