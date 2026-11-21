"""
@author: Linda Tai
將爬取的多間飯店房價數據進行視覺化分析，能夠生成價格走勢圖表，並計算「合理價格」的出現機率。
房價走勢圖表 - 將多間飯店的房價數據以折線圖展示
合理價計算 - 統計最低價的1.3倍以內的價格出現機率
"""

#plot
import matplotlib.pyplot as plt
import csv



with open('hotel-price-1month_h1_mitsui.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)   
    x1 = []
    y1 = []
    for row in rows:
        x1.append(row[0][5:]) #12/31 (year not shown)
        y1.append(int(row[2])) 

with open('hotel-price-1month_h2_intergate.csv', newline='') as csvfile2:
    rows = csv.reader(csvfile2)   
    y2 = []
    for row in rows:
        y2.append(int(row[2]))
        
with open('hotel-price-1month_h3_daiwa-roynet.csv', newline='') as csvfile3:
    rows = csv.reader(csvfile3)   
    y3 = []
    for row in rows:
        y3.append(int(row[2]))
        


fig1 = plt.figure(figsize=(10,5), dpi=120)  #Default=>dpi=80


plt.plot(x1, y3, color = 'y', marker='o', linestyle = '--', label='h3')
plt.plot(x1, y2, color = 'yellowgreen', marker='D', linestyle = '--', label='h2')
plt.plot(x1, y1, color = 'red', marker='o', linestyle = '--', label='h1')

plt.legend(loc = 'upper right')
plt.xlabel('Date', size=20) #, color = 'blue')
plt.ylabel('Price (yen)', size=20) #, color = 'blue')

plt.title('Daily Room Rate', size=18) #, color = 'blue')

stride = 7 #每n個刻度顯示一次標籤",
plt.xticks(ticks=x1[1:(len(x1)+1):stride], labels=x1[1:(len(x1)+1):stride], fontsize=14, rotation=0)

y_upper = 85000  # 手動設定上限
plt.ylim(8000, y_upper)
max_k = y_upper // 1000
labely = [f'{i}k' for i in range(10, max_k + 1, 10)]
plt.yticks([i * 1000 for i in range(10, max_k + 1, 10)], labels=labely, fontsize=16)

plt.grid(
    visible=True,  #是否顯示網格，預設False不顯示，設定True則顯示。
    axis='x',
    #color='#c00',
    dashes=(2,2),
    linewidth=2,
    alpha=0.5) #隔線透明度，預設 1 完全不透明，設定 0 完全透明。


plt.tight_layout()
plt.savefig('hotel-price-1month_h1h2h3.png', bbox_inches='tight') 


#----------------------------------------------
#合理價出現機率

def countReasonablePrice(y_price):
    #y_price_min = min(y_price)
    y_price_len = len(y_price)
    
    #合理價 = 最低價的1.3倍
    y_price_index = [i for i in range(len(y_price)) if y_price[i] < min(y_price)*1.3 ] 
    y_price_low_count = len(y_price_index) #合理價次數
    print(f'{y_price_low_count}, {y_price_len}, {100*y_price_low_count/y_price_len:.1f}%') #合理價出現機率
    
countReasonablePrice(y1)
countReasonablePrice(y2)
countReasonablePrice(y3)
