# -*- coding: utf-8 -*-
"""
@author: Linda
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import cv2
import csv
import pandas as pd

#爬取Firenze, Italy - Uffizi博物館 線上展示數百個展品，使用截圖並裁去黑邊，存圖檔
#ref: https://lufor129.medium.com/%E6%89%8B%E6%8A%8A%E6%89%8Bpython%E7%88%AC%E8%9F%B2%E6%95%99%E5%AD%B8-%E4%BA%8C-selenium-666a9fca0bd0
url='https://artsandculture.google.com/partner/uffizi-gallery'
driver = webdriver.Chrome()
driver.get(url)


#scroll 網頁往下瀏覽
driver.execute_script("window.scrollTo(0,1500)")


pageNum=3
#Selenium IDE
#按箭頭向右移pageNum次
for i in range(pageNum):
    driver.find_element(By.CSS_SELECTOR, ".mqAyNe > .CMCEae .LKARhb").click()
    time.sleep(0.5)  #second

#全部圖片
# 直到右鍵消失，無法點擊錯誤出現代表已經往右到底
# while(True):
#     try:
#         driver.find_element(By.CSS_SELECTOR, ".mqAyNe > .CMCEae .LKARhb").click()
#         time.sleep(0.5)  #second
#     except:
#         print("Element Click Intercepted Exception")
#         break


#多個elements => class="wcg9yf"
a_nodes=driver.find_elements(By.XPATH, '//div[@class="wcg9yf"]//a')

links = []
for node in a_nodes:
    links.append(node.get_attribute("href"))

#save web links
df = pd.DataFrame(links)
df.to_csv('selenium_IDE_Art_link.csv', encoding='utf-8-sig', header=False, index=False) 



dir_name = "./art_imgs/"
# 如果資料夾不存在就新增
if(os.path.isdir(dir_name) == False):
    os.mkdir(dir_name)
    
img_xpath = '//img[@class="XkWAb-LmsqOc XkWAb-Iak2Lc"]'
title_xpath = '//h1[@class="EReoAc"]'
num=0
for link in links:
    #每個圖片的連結
    driver.get(link)
    
    try:
        # 最多等待 img_xpath 10秒，超過10秒拋出ExpectedCondition
        # 如果10秒內出現了則立即回傳給element
        # google art&culture 是 bolb比較難用requests爬
        # 所以我們用 selenium連到後截圖保存
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,img_xpath)))
        img_link = element.get_attribute("src")
        #title = driver.find_element(By.XPATH, title_xpath).text
        
        # 截圖保存
        driver.get(img_link)
        num+=1
        driver.save_screenshot(f'{dir_name}art_{num:03d}.png')
        time.sleep(0.1)  #second
        
    except:
        continue
driver.quit()


#==============================
#切出interested region


for filename in os.listdir(dir_name):
    filepath = dir_name + filename
    

    img = cv2.imread(filepath)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    ret,thresh = cv2.threshold(imgray,20,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #Bounding Rectangle
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(imgray,(x,y),(x+w,y+h),(0,0,255),2)
    
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite(dir_name + 'crop_' + filename, crop_img)



