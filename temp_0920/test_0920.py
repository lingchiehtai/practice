# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 08:49:54 2024

@author: Linda Tai

data from https://github.com/allisonhorst/palmerpenguins
分析企鵝數據集 (penguins.csv)，並使用 Seaborn 和 Matplotlib 進行可視化。
"""


import pandas as pd
import seaborn as sns  
import csv
import numpy as np
import matplotlib.pyplot as plt

with open('penguins.csv', 'r', newline='') as csvfile:
    rows = list(csv.reader(csvfile)) 
    
#data=pd.DataFrame(rows)
data=pd.DataFrame(rows[1:], columns=rows[0])

#替换字符串"NA" 為 NaN
data.replace("NA", np.nan, inplace=True)

#show the category
for i, category in enumerate(data['species'].unique()):
    print(i, category)
for i, category in enumerate(data['island'].unique()):
    print(i, category)
for i, category in enumerate(data['sex'].unique()):
    print(i, category)

#delete data:nan
rawdata = data.copy()
data = data.dropna()

# 將類別名稱map to 數字
species_mapping = {'Adelie': 0, 'Gentoo': 1, 'Chinstrap': 2}
data['species'] = data['species'].map(species_mapping)
print(data[['species']].tail())

island_mapping = {'Torgersen': 0, 'Biscoe': 1, 'Dream': 2}
data['island'] = data['island'].map(island_mapping)
print(data[['island']].tail())

sex_mapping = {'male': 0, 'female': 1}
data['sex'] = data['sex'].map(sex_mapping)
print(data[['sex']].tail())

#str convert to 數值
cols_to_convert = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
data[cols_to_convert] = data[cols_to_convert].apply(pd.to_numeric, errors='coerce')


#plot 畫出不同參數之間的關係，分別用species, island, sex 標出不同顏色
sns.pairplot(data[:], diag_kind='kde')

sns.pairplot(data[:], diag_kind='kde', hue='species')
sns.pairplot(data[:], diag_kind='kde', hue='island')
sns.pairplot(data[:], diag_kind='kde', hue='sex')

#從圖中看出 對於不同的species，似乎可以分為不同區域

#matplotlib.pyplot
#Depth and Length for Diff. Species
plt.figure(figsize=(10,6), dpi=120)
plt.axes([0.12, 0.16, 0.85, 0.75])

x = data['bill_length_mm']
y = data['bill_depth_mm']
z = data['species']

plt.scatter(x[z==0], y[z==0], color='red', label='species:Adelie')
plt.scatter(x[z==1], y[z==1], color='green', label='species:Gentoo')
plt.scatter(x[z==2], y[z==2], color='blue', label='species:Chinstrap')

plt.xlabel('Bill Length (mm)', size=24)
plt.ylabel('Bill Depth (mm)', size=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Depth and Length for Diff. Species', size=20)
plt.legend()

plt.savefig('plot_Depth_Length_Diff_Species.png')
