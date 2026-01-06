

#plot
import matplotlib.pyplot as plt
import csv



with open('hotel-price-longPeriod_h1_mitsui.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)   
    x1 = []
    y1 = []
    for row in rows:
        x1.append(row[0][5:]) # 2024/10/31 => 10/31 (year not shown)
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
        


fig1 = plt.figure(figsize=(12,6), dpi=120)  #Default=>dpi=80
plt.axes([0.10, 0.15, 0.85, 0.75]) #axes( [x, y, width, height] ): x,y為和左下角的相對位置
plt.plot(x1, y1, color = 'darkred', marker='.', linestyle = '--', label='h1')
#plt.plot(x1, y2, color = 'darkblue', marker='.', linestyle = '--', label='h2')
#plt.plot(x1, y3, color = 'darkblue', marker='.', linestyle = '--', label='h3')


stride = 7 #每n個刻度顯示一次標籤\n",
stride2=stride*2
plt.xticks(ticks=x1[4:(len(x1)+1):stride2], labels=x1[4:(len(x1)+1):stride2], fontsize=14, rotation=0)
plt.xlim(0, len(y1)-1)
plt.ylim(5000, 85000)
labely= ['10k','20k','30k','40k','50k','60k','70k','80k']
plt.yticks([10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000], labels=labely, fontsize=16)
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

#plt.savefig('hotel-price-longPeriod_1.png') 



##### Average price for 2 weeks
yprice = y1
div=len(yprice)//14
avg1=[0]*len(yprice)
for i in range(div-1):
    start=5+14*i
    avg1[start+6] = int(sum(yprice[start:start+14])/14)

plt.bar(x1, avg1, width=8.0, label='Avg.')

plt.legend(loc = 'best') #'upper right'
plt.xlabel('Date', size=20) #, color = 'blue')
plt.ylabel('Price (yen)', size=20) #, color = 'blue')

plt.title('Daily Room Rate', size=14) #, color = 'blue')

plt.savefig('hotel-price-longPeriod_avg_1.png') 




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
