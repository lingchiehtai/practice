"""
@author: Linda Tai
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
        
with open('hotel-price-1month_h4_nohga.csv', newline='') as csvfile4:
    rows = csv.reader(csvfile4)   
    y4 = []
    for row in rows:
        y4.append(int(row[2]))

       

with open('hotel-price-1month_h5_cross.csv', newline='') as csvfile5:
    rows = csv.reader(csvfile5)   
    y5 = []
    for row in rows:
        y5.append(int(row[2])) 

with open('hotel-price-1month_h6_m-39-s.csv', newline='') as csvfile6:
    rows = csv.reader(csvfile6)   
    y6 = []
    for row in rows:
        y6.append(int(row[2]))
        
with open('hotel-price-1month_h7_fresa-inn.csv', newline='') as csvfile7:
    rows = csv.reader(csvfile7)   
    y7 = []
    for row in rows:
        y7.append(int(row[2]))
        
with open('hotel-price-1month_h8_prince-smart.csv', newline='') as csvfile8:
    rows = csv.reader(csvfile8)   
    y8 = []
    for row in rows:
        y8.append(int(row[2]))


fig1 = plt.figure(figsize=(10,5), dpi=120)  #Default=>dpi=80


plt.plot(x1, y3, color = 'y', marker='o', linestyle = '--', label='h3')
plt.plot(x1, y2, color = 'yellowgreen', marker='D', linestyle = '--', label='h2')
plt.plot(x1, y1, color = 'red', marker='o', linestyle = '--', label='h1')

plt.legend(loc = 'upper right')
plt.xlabel('Date', size=20) #, color = 'blue')
plt.ylabel('Price (yen)', size=20) #, color = 'blue')

plt.title('Daily Room Rate', size=18) #, color = 'blue')

stride = 7 #每n個刻度顯示一次標籤\n",
plt.xticks(ticks=x1[1:62:stride], labels=x1[1:62:stride], fontsize=16, rotation=0)
plt.ylim(5000, 85000)
labely= ['10k','20k','30k','40k','50k','60k','70k','80k']
plt.yticks([10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000], labels=labely, fontsize=16)

plt.grid(
    visible=True,  #是否顯示網格，預設False不顯示，設定True則顯示。
    axis='x',
    #color='#c00',
    dashes=(2,2),
    linewidth=2,
    alpha=0.5) #隔線透明度，預設 1 完全不透明，設定 0 完全透明。


plt.savefig('hotel-price-1month_1.png') 


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
