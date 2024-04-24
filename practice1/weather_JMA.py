# -*- coding: utf-8 -*-
"""
@author: Linda Tai
#從日本氣象廳(JMA)網頁讀取某地某年的氣象資料， 將表格內容存成csv檔案。
 再用matplotlib畫出每月趨勢圖
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

loc1 = 'prec_no=86&block_no=47819' #熊本
loc2 = 'prec_no=56&block_no=47605' #金沢
loc3 = 'prec_no=31&block_no=47575' #青森
loc4 = 'prec_no=14&block_no=47412' #札幌

head = 'https://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s1.php?'
tail = '&year=2023&month=1&day=1&view='

url1 = head + loc1 + tail
url2 = head + loc2 + tail
url3 = head + loc3 + tail
url4 = head + loc4 + tail


#讀取網頁中的表格資料
def getTableData(url):
    web = requests.get(url)    
    web.encoding='utf-8'       # 網頁編碼 
    soup = BeautifulSoup(web.text, "html.parser")   
    city = soup.find('h3', style="padding:0px;margin-bottom:0px").text.split("\u3000")[0].split("（")[0]  #\u3000 是全角的空白符   
    
    data = pd.read_html(url, header=0, keep_default_na=True)  #keep_default_na: 是否去除空白值
    df=data[0]
    #表格中的---換成0
    df['雪(cm)'] = df['雪(cm)'].str.replace('--', '0')
    df['雪(cm).1'] = df['雪(cm).1'].str.replace('--', '0')
    df['雪(cm).2'] = df['雪(cm).2'].str.replace('--', '0')
    return df,city


df1, city1 = getTableData(url1)
df2, city2 = getTableData(url2)
df3, city3 = getTableData(url3)
df4, city4 = getTableData(url4)


#將表格內容存成csv檔案
df1.to_csv(f'weatherJMA_Data_{city1}.csv', encoding='utf-8-sig')
df2.to_csv(f'weatherJMA_Data_{city2}.csv', encoding='utf-8-sig')
df3.to_csv(f'weatherJMA_Data_{city3}.csv', encoding='utf-8-sig')
df4.to_csv(f'weatherJMA_Data_{city4}.csv', encoding='utf-8-sig')


#Avg. temp
def dataFrame_avgTemp(dataTemp):
    ytemp = dataTemp.iloc[2:, 7].values
    ytemp = [float(ytemp[i]) for i in range(len(ytemp))]
    return ytemp

y1 = dataFrame_avgTemp(df1)
y2 = dataFrame_avgTemp(df2)    
y3 = dataFrame_avgTemp(df3)
y4 = dataFrame_avgTemp(df4)



#某一年 幾個不同city的avg. temp ==========================================
fig1  = plt.figure(figsize=(10,6))
x_month=range(1,13)

plt.plot(x_month, y1, color = 'red', label='city1', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_month, y2, color = 'blue', label='city2', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_month, y3, color = 'green', label='city3', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_month, y4, color = 'purple', label='city4', marker='o', markersize=12, linestyle = '--', linewidth=3)

plt.legend(loc = 'upper left', fontsize=18)
plt.xlabel('Month', fontsize=26) 
plt.ylabel('Temperature (℃)',fontsize=26) 
#plt.title('Avg. Temperature', fontsize=24)
plt.xlim(0.5, 12.5)           
plt.ylim(-5, 35)
plt.xticks(range(1,13,1), fontsize=20)
plt.yticks(fontsize=20)
plt.grid(visible=True, axis='y', dashes=(2,2), linewidth=3, alpha=0.6) #color='#c00'
plt.savefig('weatherJMA_cities_avg_Temp.png') #白底




#某一city: 3年來的data ===================================================
url2022 = head + loc4 + '&year=2022&month=1&day=1&view='
url2021 = head + loc4 + '&year=2021&month=1&day=1&view='
url2020 = head + loc4 + '&year=2020&month=1&day=1&view='
df2022,city4 = getTableData(url2022)
df2021,city4 = getTableData(url2021)
df2020,city4 = getTableData(url2020)

#snow(cm)
def dataFrame_snow(dataF):
    ysnow = dataF.iloc[2:, 21].values
    ysnow = [float(ysnow[i]) for i in range(len(ysnow))]
    yshift10to4 =[ysnow[9],ysnow[10],ysnow[11],ysnow[0],ysnow[1],ysnow[2],ysnow[3]] #10-12, 1~4月
    return yshift10to4

ysnow2023 = dataFrame_snow(df4)
ysnow2022 = dataFrame_snow(df2022)
ysnow2021 = dataFrame_snow(df2021)
ysnow2020 = dataFrame_snow(df2020)

x_shift = ['10','11','12','1','2','3','4']
fig2 = plt.figure(figsize=(10,6))
plt.plot(x_shift, ysnow2023, color = 'blue', label='2023', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_shift, ysnow2022, color = 'olive', label='2022', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_shift, ysnow2021, color = 'green', label='2021', marker='o', markersize=12, linestyle = '--', linewidth=3)
plt.plot(x_shift, ysnow2020, color = 'deepskyblue', label='2020', marker='o', markersize=12, linestyle = '--', linewidth=3)

plt.legend(loc = 'upper right', fontsize=18)
plt.xlabel('Month', fontsize=26) 
plt.ylabel('Snowfall (cm)',fontsize=26) 
#plt.title('Monthly Snowfall', fontsize=24)
#plt.xlim(0.5, 12.5)           
#plt.ylim(0, 70)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(visible=True, axis='y', dashes=(2,2), linewidth=3, alpha=0.6) #color='#c00'
plt.savefig('weatherJMA_Snowfall.png') #白底









