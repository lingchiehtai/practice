import requests
import pandas as pd
import time
from urllib.parse import quote
import os

filename = 'jobsearch_data104.xlsx'

list1 = []
output = 0
jobkind = '資料工程師'
pageMax = 2

# 加入 Headers 模擬瀏覽器，避免被擋
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.104.com.tw/jobs/search/'
}

# 建立 Session 以保持 Cookies
ss = requests.Session()
ss.get(f'https://www.104.com.tw/jobs/search/?keyword={quote(jobkind)}&jobsource=index_s', headers=headers)


for ipageNum in range(1, pageMax + 1):
    #104 API
    url = 'https://www.104.com.tw/jobs/search/api/jobs'
    
    params = {
        'jobsource': 'm_joblist_search',     # 從你提供的 URL 來的
        'keyword': jobkind,
        'order': 15,                         # 15 通常代表「最新」
        'page': ipageNum,
        'pagesize': 20                       # 每頁預設 20 筆
    }
    
    headers['Referer'] = f'https://www.104.com.tw/jobs/search/?keyword={quote(jobkind)}'
    
    response = ss.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"page: {ipageNum}, 狀態碼錯誤: {response.status_code}")
        continue

    try:
        data = response.json()
        print("=== 回傳的 keys ===")
        print(list(data.keys()))
        # if 'data' in data:
        #     print("data 裡面的 keys:")
        #     print(list(data['data'].keys()))
    except requests.exceptions.JSONDecodeError:
        print(f"page: {ipageNum}, 不是有效的 JSON")
        print("回應內容:", response.text[:500])  # 只印前面500字
        continue

    # ─────────────── 這裡是主要修改 ───────────────
    # 新的資料位置：data['data']['jobList']['job']
    if 'data' not in data or not isinstance(data['data'], list):
        print(f"page: {ipageNum}, data 不是列表或不存在")
        continue

    jobs = data['data']
    # 印出第一筆資料的所有欄位名稱，幫助我們知道有哪些欄位可以用
    if jobs:  # 如果有資料
        print("第一筆職缺的所有欄位：")
        print(list(jobs[0].keys()))

    print(f'page: {ipageNum}, 找到 {len(jobs)} 筆職缺')
    
    for job in jobs:
        try:
            cpName = job.get('custName', '')
            jobTitle = job.get('jobName', '')
            print(cpName, end=' ')
            
            date = job.get('appearDate', '')
            jobLocation = job.get('jobAddrNoDesc', '') + ' ' + job.get('jobAddress', '')
            period_code = job.get('period', '')
            Experience = f"{int(period_code) - 1}年以上" if period_code and period_code != '0' else '不拘'
            
            #Education = job.get('optionEdu', '')         # 現在叫 optionEdu
            edu_code = job.get('optionEdu', [])

            if isinstance(edu_code, list) and edu_code:
                edu_map = {
                    1: '高中職以下',
                    2: '高中職',
                    3: '專科',
                    4: '大學',
                    5: '碩士',
                    6: '博士'
                }
                
                # 先檢查是否全部六種 → 不拘
                if set(edu_code) == {1, 2, 3, 4, 5, 6}:
                    Education = '不拘'
                
                else:
                    # 產生學歷文字列表
                    edu_list = []
                    for code in edu_code:
                        edu_list.append(edu_map.get(code, f'未知({code})'))
                    
                    # 再檢查「OO以上」的情況
                    if set(edu_code) == {3, 4, 5, 6}:
                        Education = '專科以上'
                    elif set(edu_code) == {4, 5, 6}:
                        Education = '大學以上'
                    else:
                        Education = '、'.join(edu_list)

            else:
                Education = '不拘'

            # Salary
            salary_low = job.get('salaryLow', '')
            salary_high = job.get('salaryHigh', '')

            if salary_low and salary_high and salary_low != '0' and salary_high != '0':
                low = int(salary_low)
                high = int(salary_high)
                if high >= 9999990:  # 或你觀察到的實際極大值
                    jobSalary = f"月薪 {low:,}元以上"
                elif low >= 500000:
                    jobSalary = f"年薪 {low:,} ~ {high:,}元"
                else:
                    jobSalary = f"月薪 {low:,} ~ {high:,}元"
            elif salary_low and salary_low != '0':
                low = int(salary_low)
                jobSalary = f"月薪 {low:,}元以上"

            else:
                jobSalary = job.get('salaryDesc') or '待遇面議'

            print(f"薪資描述: {jobSalary}")
            jobcontent = job.get('description', '')

            link_info = job.get('link', {})
            link_path = link_info.get('job', '') if isinstance(link_info, dict) else ''
            jobWebsite = link_path if link_path.startswith('http') else f"https://{link_path.lstrip('/')}" if link_path else ''
            cpKind = job.get('coIndustryDesc', '')

            time.sleep(0.3)
                
            list1.append([date, jobTitle, cpName, cpKind, jobLocation, jobSalary, Experience, Education, jobcontent, jobWebsite])
            output += 1

            print('OK')
            
        except Exception as e:
            print(f'處理單筆資料時發生錯誤: {e}')
            continue
    
# 欄位名稱保持不變
# 欄位名稱保持不變
column1 = ['發佈日期','職務名稱','公司名稱','公司類別','工作地點','薪資','工作經驗','學歷', '工作內容','工作網址']    
#df = pd.DataFrame(list1, columns=column1)

df_new = pd.DataFrame(list1, columns=column1)

# 如果檔案存在，先讀取舊資料再合併
if os.path.exists(filename):
    try:
        df_old = pd.read_excel(filename)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    except Exception as e:
        print(f"讀取舊檔案失敗：{e}")
        df_combined = df_new
else:
    df_combined = df_new

# 寫回 Excel（會覆蓋，但內容已包含舊+新）
df_combined.to_excel(filename, index=False, engine='openpyxl')
print(f"已更新檔案：{filename} （總數：{len(df_combined)} 筆）")
print(f"新增： {output} 筆資料")