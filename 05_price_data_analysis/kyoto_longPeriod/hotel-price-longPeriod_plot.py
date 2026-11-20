#plot
import matplotlib.pyplot as plt
import csv
import math

with open('hotel-price-longPeriod_h1_mitsui.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)   
    x1 = []
    y1 = []
    for row in rows:
        x1.append(row[0][5:]) # 2024/10/31 => 10/31 (去除年份的 x1)
        y1.append(int(row[2])) 


with open('hotel-price-longPeriod_h2_intergate.csv', newline='') as csvfile2:
    rows = csv.reader(csvfile2)   
    y2 = []
    for row in rows:
        y2.append(int(row[2]))
        
with open('hotel-price-longPeriod_h3_daiwa-roynet.csv', newline='') as csvfile3:
    rows = csv.reader(csvfile3)
    y3 = []
    for row in rows:
        y3.append(int(row[2]))
        


# ==============================================================
# 選擇要繪製的飯店（只需在此處切換：'h1', 'h2', 或 'h3'）
target_hotel = 'h1'
# 手動指定 Y 軸上限（例如 85000 或 85；設為 None 則依資料自動計算）
Max_Y = 85; None
# ==============================================================


hotel_configs = {
    'h1': {'y': y1, 'color': 'darkviolet', 'label': 'h1'},
    'h2': {'y': y2, 'color': 'darkviolet', 'label': 'h2'},
    'h3': {'y': y3, 'color': 'darkviolet', 'label': 'h3'},  # 明顯的紫色 (亦可使用 'purple')
}
current_y = hotel_configs[target_hotel]['y']
current_color = hotel_configs[target_hotel]['color']
current_label = hotel_configs[target_hotel]['label']

fig1 = plt.figure(figsize=(12,6), dpi=120)  #Default=>dpi=80
plt.axes([0.10, 0.15, 0.85, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, current_y, color=current_color, marker='.', linestyle='--', label=current_label)


stride = 7 #每n個刻度顯示一次標籤\n",
stride2=stride*2
plt.xticks(ticks=x1[4:(len(x1)+1):stride2], labels=x1[4:(len(x1)+1):stride2], fontsize=14, rotation=0)
plt.xlim(0, len(current_y)-1)


manual_y_max = Max_Y 

if manual_y_max is not None:
    y_upper = manual_y_max * 1000 if manual_y_max < 1000 else manual_y_max
else:
    # 依房價最大值自動計算上限（每 5000 一級，例如 76000 -> 80000）
    y_upper = math.ceil(max(current_y) / 5000) * 5000

plt.ylim(5000, y_upper)
max_k = y_upper // 1000
labely = [f'{i}k' for i in range(10, max_k + 1, 10)]
plt.yticks([i * 1000 for i in range(10, max_k + 1, 10)], labels=labely, fontsize=16)
# plt.ylim(5000, 35000)
# labely= ['10k','20k','30k']
# plt.yticks([10000, 20000, 30000], labels=labely, fontsize=16)

plt.yticks(fontsize=16)


plt.grid(
    visible=True,  #是否顯示網格，預設False不顯示，設定True則顯示。
    axis='x',
    #color='#c00',
    dashes=(2,2),
    linewidth=2,
    alpha=0.5) #隔線透明度，預設 1 完全不透明，設定 0 完全透明。



##### Average price for 2 weeks
yprice = current_y
div = len(yprice) // 14
avg1 = [0] * len(yprice)
for i in range(div - 1):
    start = 4 + 14 * i
    avg1[start + 7] = int(sum(yprice[start:start + 14]) / 14)

# 最後剩餘區間：雖不滿 14 天，但大於等於 7 天也加入平均價
rem_start = 4 + 14 * (div - 1)
rem_len = len(yprice) - rem_start
if rem_len >= 7:
    avg1[rem_start + rem_len // 2] = int(sum(yprice[rem_start:]) / rem_len)

plt.bar(x1, avg1, width=8.0, label='Avg.')

plt.legend(loc = 'best') #'upper right'
plt.xlabel('Date', size=20) #, color = 'blue')
plt.ylabel('Price (yen)', size=20) #, color = 'blue')

plt.title('Daily Room Rate', size=14) #, color = 'blue')

plt.savefig(f'hotel-price-longPeriod_avg_{target_hotel}.png') 




# ##合理價出現機率
# def countReasonablePrice(y_price):
#     #y_price_min = min(y_price)
#     y_price_len = len(y_price)
    
#     #合理價=最低價的1.3倍
#     y_price_index = [i for i in range(len(y_price)) if y_price[i] < min(y_price)*1.3 ] 
#     y_price_low_count = len(y_price_index) #合理價次數
#     print(f'{y_price_low_count}, {y_price_len}, {100*y_price_low_count/y_price_len:.1f}%') #合理價出現機率

# #1~2 月
# y1p = y1[92:151]
# y2p = y2[92:151]
# y3p = y3[92:151]
# countReasonablePrice(y1p)
# countReasonablePrice(y2p)
# countReasonablePrice(y3p)
