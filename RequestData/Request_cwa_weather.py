# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 22:31:07 2024

@author: Linda
"""

# 雷達回波圖 (from JSON file) => 存檔
#https://steam.oxxostudio.tw/category/python/spider/radar.html

import requests
import datetime

url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization=rdec-key-123-45678-011121314&format=JSON'
data = requests.get(url)  
#print(data.text)
data_json = data.json()
#找到圖檔網址
picURL = data_json['cwaopendata']['dataset']['resource']['ProductURL'] 
print('雷達整合回波圖-臺灣(鄰近地區)_無地形',picURL)

DateTime = data_json['cwaopendata']['dataset']['DateTime'].split("T")
print(DateTime)
date = DateTime[0][0:4]+DateTime[0][5:7]+DateTime[0][8:]
time = DateTime[1][0:2]+DateTime[1][3:5]
print(date, time)


#使用 requests 模組下載圖檔
picFile = requests.get(picURL, allow_redirects=True)
# now = datetime.datetime.now()
# picFilename='pic_' + now.strftime("%Y%m%d_%H%M")+'.png'
picFilename=f'pic_雷達回波圖_{date}_{time}.png'
print(picFilename)
with open(picFilename, "wb") as f:
    f.write(picFile.content)
    
    
#===============================
#使用 requests 模組下載cwa網頁中的 颱風警報路徑圖
timeTW = datetime.datetime.now()

picURL = "https://www.cwa.gov.tw/Data/typhoon/TY_WARN/B20.png"
picFile = requests.get(picURL, allow_redirects=True)
picFilename='pic_颱風警報_' + timeTW.strftime("%Y%m%d_%H%M") +'.png'
print(picFilename)
with open(picFilename, "wb") as f: 
    f.write(picFile.content)

