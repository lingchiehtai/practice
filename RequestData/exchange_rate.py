# -*- coding: utf-8 -*-
"""
@author: Linda Tai
"""

#爬取臺灣銀行牌告匯率   

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

df1=pd.DataFrame(list1)
USD_buy=df1.iloc[0,1]
USD_sell=df1.iloc[0,2]
JPY_buy=df1.iloc[7,1]
JPY_sell=df1.iloc[7,2]
EUR_buy=df1.iloc[13,1]
EUR_sell=df1.iloc[13,2]

with open('exchange_rate_history.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    #writer.writerow(['date', 'USDbuy', 'USDsell', 'JPYbuy', 'JPYsell', 'EURbuy', 'EURsell'])
    writer.writerow([dd, USD_buy, USD_sell, JPY_buy, JPY_sell, EUR_buy, EUR_sell])


#plot
