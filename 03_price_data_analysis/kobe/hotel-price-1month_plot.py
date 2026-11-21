

#plot
import matplotlib.pyplot as plt
import csv
import math



with open('hotel-price-1month_k1_royalpark.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)   
    x1 = []
    y1 = []
    for row in rows:
        x1.append(row[0][5:]) #12/31 (year not shown)
        y1.append(int(row[2])) 


with open('hotel-price-1month_k2_daiwa.csv', newline='') as csvfile2:
    rows = csv.reader(csvfile2)   
    y2 = []
    for row in rows:
        y2.append(int(row[2]))
        
with open('hotel-price-1month_k3_tokyu-kobe.csv', newline='') as csvfile3:
    rows = csv.reader(csvfile3)
    y3 = []
    for row in rows:
        y3.append(int(row[2]))
        


fig1 = plt.figure(figsize=(10,5), dpi=120)  #Default=>dpi=80
#plt.axes([0.10, 0.15, 0.85, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, y1, color = 'darkred', marker='D', linestyle = '--', label='k1')
plt.plot(x1, y2, color = 'g', marker='o', linestyle = '--', label='k2')
plt.plot(x1, y3, color = 'b', marker='o', linestyle = '--', label='k3')


stride = 7 #每n個刻度顯示一次標籤\n",

plt.xticks(ticks=x1[1:(len(x1)+1):stride], labels=x1[1:(len(x1)+1):stride], fontsize=14, rotation=0)
#plt.xlim(0, len(y1)-1)

# 可手動指定上限 (例如 40 或 40000)，若設為 None 則自動計算
manual_y_max = None

current_y = y1 + y2 + y3
if manual_y_max is not None:
    y_upper = manual_y_max * 1000 if manual_y_max < 1000 else manual_y_max
else:
    # 依房價最大值自動計算上限（每 5000 一級，例如 76000 -> 80000）
    y_upper = math.ceil(max(current_y) / 5000) * 5000

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

plt.legend(loc = 'best') #'upper right'
plt.xlabel('Date', size=20) #, color = 'blue')
plt.ylabel('Price (yen)', size=20) #, color = 'blue')

plt.title('Daily Room Rate', size=18) #, color = 'blue')

plt.tight_layout()
plt.savefig('hotel-price-1month_k1k2k3.png', bbox_inches='tight') 



########################
##合理價出現機率

def countReasonablePrice(y_price):
    #y_price_min = min(y_price)
    y_price_len = len(y_price)
    
    #合理價=最低價的1.3倍
    y_price_index = [i for i in range(len(y_price)) if y_price[i] < min(y_price)*1.3 ] 
    y_price_low_count = len(y_price_index) #合理價次數
    print(f'{y_price_low_count}, {y_price_len}, {100*y_price_low_count/y_price_len:.1f}%') #合理價出現機率
    
countReasonablePrice(y1)
countReasonablePrice(y2)
countReasonablePrice(y3)


