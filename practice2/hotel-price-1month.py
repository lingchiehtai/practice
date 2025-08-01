# -*- coding: utf-8 -*-
"""
@author: Linda Tai
觀察某飯店某月份的房價趨勢
ex:某天的房價網址 https://www.booking.com/hotel/jp/mitsui-garden-kyoto-kawaramachi-jokyoji.zh-tw.html?
checkin=2024-06-22&checkout=2024-06-23&do_availability_check=1&group_adults=2&group_children=0&selected_currency=hotel_currency

"""

import requests
from bs4 import BeautifulSoup
import csv
import time


def GetRoomPrice(bookURL, roomTypeBlockID):
    
    try:
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Cookie" : "pcm_consent=analytical%3Dtrue%26countryCode%3DTW%26consentId%3D875e90ea-7348-4330-b5d1-03faddf8187a%26consentedAt%3D2024-03-12T06%3A20%3A03.629Z%26expiresAt%3D2024-09-08T06%3A20%3A03.629Z%26implicit%3Dtrue%26marketing%3Dtrue%26regionCode%3DKHH%26regulation%3Dnone%26legacyRegulation%3Dnone; px_init=0; pcm_personalization_disabled=0; bkng_sso_auth=CAIQsOnuTRpm6tVsG2KF9N49yWQYBp24ROpDXRcMoo7jp4HIJn4mQVdrashUBtSj3dX3CCKUr04n8fJmNdkT127QeTgyuV1i0AHm1UJYW1K6pbV4p8oYKExHP1hN0rSqYn3dnGpHha2uRkFY4Mwz; cors_js=1; aws-waf-token=44fae8e6-45ef-4b17-ba42-345794e1f574:AAoAuzYku6fmAAAA:QHuaUufa9qPHmPHdGS2ZohGK34xjJyhfFTWBgYlhynR2gGi5KhsNKShr/k93bQ08hLb2knWXrR5+dAHuJjOmb+8N4XW0RMZ7hhne7ZFaxuaHJsaWyn5wxkQXJHLWSxSNCnmiLZcsHo5z96MXvAW/DvdTweHupHSI5sgIiChfE2zoUjBOW33E/m6fyT8RFYSU03ehOCOm5D+GAkUoZ/TuwTC5j6FyJt2cfOAC7UO6Z6MZtoTas+7Jio1nklJLNcZ7mD4c; bkng=11UmFuZG9tSVYkc2RlIyh9YSvtNSM2ADX0BnR0tqAEmjtAzvsn8OY9T4VXEHFF8cK9IuYdVsrhjpXynuy%2BITrWXvd169hYatAr5KnCQBtj6PXAuvNa6k02m7cMa%2Ff0AIcktOZS4yOj3To4hlXMYYwmM%2Bc%2B9Eh4jif%2BvucA1v%2BliBQJw2wf9yf4qazwETH2xwrQmq3RAabxuJHLsxc6xg%2BLgA%3D%3D; lastSeen=1712726850435"
        }
        res = requests.get(bookURL, headers=headers)        
        soup=BeautifulSoup(res.text,'html.parser')  
        #print(res.status_code)
        table = soup.find('tr', {'data-block-id': roomTypeBlockID}) #鎖定某一房型    
        RoomType = table.find('span', class_='hprt-roomtype-icon-link').text.strip()
        
        text1 = table.find('span', class_='prco-valign-middle-helper').text.strip()
        RoomPrice = text1[1:((len(text1)-4))] + text1[-3:] #不包含幣值的符號 ¥
        time.sleep(0.1)
    except:
        RoomType = 'None'
        RoomPrice = '0'
    return RoomType, RoomPrice


#改變網址參數以取得不同飯店/不同日期的房價
mon1 = 12  #需指定的參數 #某月份的房價
year = 2024

dict1 = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31} #每個月有幾天
StartDate = 1
EndDate = dict1[mon1]

with open('hotel-price-1month.csv', 'a', newline="") as file1:
    writer = csv.writer(file1)
    
    y1 = year
    y2 = y1
    
    for date1 in range(StartDate, EndDate+1):
        if date1 == dict1[mon1]:
            date2 = 1
            if mon1 ==12:
                mon2 = 1
                y2 = y1 + 1
            else:
                mon2 = mon1+1
            
        else:
            mon2 = mon1
            date2 = date1+1
        
        #h1
        # hotel = 'https://www.booking.com/hotel/jp/mitsui-garden-kyoto-kawaramachi-jokyoji.zh-tw.html?'
        # dataBlockID = '637479308_254974238_0_2_0'
        #h2
        # hotel = 'https://www.booking.com/hotel/jp/hotel-intergate-kyoto-shijoshinmachi.zh-tw.html?'
        # dataBlockID = '274983202_109599197_2_2_0'
        #h3
        hotel = 'https://www.booking.com/hotel/jp/daiwa-roynet-kyoto-shijyo-karasuma.zh-tw.html?'
        dataBlockID = '40532402_169540716_2_2_0'       
        
        #h4
        # hotel = 'https://www.booking.com/hotel/jp/nohga-kiyomizu-kyoto.zh-tw.html?'
        # dataBlockID = '759821601_358316618_2_2_0'
        #h5
        # hotel = 'https://www.booking.com/hotel/jp/cross-hotel-kyoto.zh-tw.html?'
        # dataBlockID = '349634563_166386087_2_2_0'
        #h6
        #hotel = 'https://www.booking.com/hotel/jp/the-m-39-s-kyoto.zh-tw.html?'
        #dataBlockID = '697140103_287871616_2_0_0'        
        #h7
        # hotel = 'https://www.booking.com/hotel/jp/sotetsu-fresa-inn-kyoto-kiyomizu-gojo.zh-tw.html?'
        # dataBlockID = '790222401_338731453_2_2_0'
        #h8
        # hotel = 'https://www.booking.com/hotel/jp/prince-smart-inn-kyotosanjo.zh-tw.html?'
        # dataBlockID = '893551101_371045355_2_0_0'
        
        #h9
        # hotel = 'https://www.booking.com/hotel/jp/the-royal-park-hotel-kyoto-umekoji.zh-tw.html?'
        # dataBlockID = '640664901_376974120_0_10_0'
        #h10
        # hotel = 'https://www.booking.com/hotel/jp/hoterurisorutoriniteijing-du-yu-chi-fu-wu-ting.zh-tw.html?'
        # dataBlockID = '295398901_387761285_0_2_0'
        
        URL = hotel + f'checkin={y1}-{mon1:02d}-{date1:02d}&checkout={y2}-{mon2:02d}-{date2:02d}&do_availability_check=1&group_adults=2&group_children=0&selected_currency=hotel_currency'           
    
        roomType, roomPrice = GetRoomPrice(URL, dataBlockID)
        date = f'{year}/{mon1:02d}/{date1:02d}'
        writer.writerow([date, roomType, roomPrice])
        print(date)

print('Finished!')

