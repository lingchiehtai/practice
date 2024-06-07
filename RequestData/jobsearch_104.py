# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:15:45 2024

@author: Linda
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time



list1 = []
jobkind = '數據python'
pageMax=6
for ipageNum in range(1,pageMax):
    baseurl=f'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={jobkind}&page={str(ipageNum)}'
    html = requests.get(baseurl)
    soup = BeautifulSoup(html.text, 'lxml')
    jobs = soup.find_all('div', class_='b-block__left')
    print('page:', ipageNum)
    
    for i in range(len(jobs)):
        #每一筆資料
       
        try:
            cpName = jobs[i].find_all('a')[1].get('title').split("\n")[0].split("：")[1]
            print(cpName, end=' ')
            date = jobs[i].find('span', class_='b-tit__date').text.strip()
            jobTitle =jobs[i].find('a').text
    
            cpKind = jobs[i].find_all('li')[2].text
            jobLocation = jobs[i].find_all('li')[3].text
            Experience = jobs[i].find_all('li')[4].text
            Education = jobs[i].find_all('li')[5].text
            
            try:
                jobSalary = jobs[i].find('span', class_='b-tag--default').text
                print('Salary type: 1', end=', ') #待遇面議
            except:
                jobSalary = jobs[i].find('a', class_='b-tag--default').text
                print('Salary type: 2', end=', ') #有列出salary
            jobcontent = jobs[i].find('p', class_='job-list-item__info b-clearfix b-content').text
            
            jobWebsite = 'http:' + jobs[i].find_all('a')[0].get('href')
            time.sleep(0.5)
                  
            list1.append([date, jobTitle,cpName,cpKind,jobLocation,jobSalary,Experience,Education,jobcontent,jobWebsite])
            print(i+1, 'is OK')
            
        except:
            print(i+1, 'NONE !!!')
            pass
    
column1=['發佈日期','職務名稱','公司名稱','公司類別','工作地點','薪資','工作經驗','學歷', '工作內容','工作網址']    
df = pd.DataFrame(list1, columns = column1)

df.to_excel('jobsearch_data104.xlsx', header=True, index=False)