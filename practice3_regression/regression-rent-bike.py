# -*- coding: utf-8 -*-
"""
@author: Linda
   
1. 準備資料：載入並清理首爾自行車租借資料，再將其分為訓練集與測試集。   
2. 訓練模型：使用TensorFlow/Keras 建立一個深度神經網路(DNN)迴歸模型來預測自行車的租借數量。
3. 評估與與視覺化：評估模型準確度、將結果視覺化成圖表，並儲存訓練好的模型。
"""

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import seaborn as sns  

#dataset #https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand
#Import the dataset 
from ucimlrepo import fetch_ucirepo   
  
# fetch dataset 
seoul_bike_sharing_demand = fetch_ucirepo(id=560) 

#pandas dataframes
dataset = seoul_bike_sharing_demand.data.original

rawdata = dataset.copy()
# # data (as pandas dataframes) 
# print(seoul_bike_sharing_demand.variables) 

# print(seoul_bike_sharing_demand.data) 
dataset.tail()
dataset.isna().sum()  #統計 np.nan 數量

"""### 不同参数之間的關係"""
sns.pairplot(dataset[['Rented Bike Count', 'Hour', 'Temperature','Humidity','Wind speed','Visibility']], diag_kind='kde')



#丟掉不要的columns
dataset.pop('Date')
dataset.pop('Functioning Day')
dataset.pop('Holiday')
dataset.pop('Seasons')

dataset.pop('Dew point temperature')
dataset.pop('Solar Radiation')
dataset.pop('Rainfall')
dataset.pop('Snowfall')

#只取Rented Bike Count 不等於0的有效資料
dataset= dataset[dataset['Rented Bike Count']>0]


"""拆開分為training and testing dataset"""
train_dataset = dataset.sample(frac=0.85, random_state=1)
test_dataset = dataset.drop(train_dataset.index)

"整體統計info "
train_dataset.describe().transpose()
train_dataset.describe().transpose()[['mean', 'std', 'max', 'min']]


"""將目標 "label" 從dataset中分離"""
train_features = train_dataset.copy()
test_features = test_dataset.copy()

"""目標 "label" = 'Rented Bike Count'  """
train_labels = train_features.pop('Rented Bike Count')
test_labels = test_features.pop('Rented Bike Count')




"""使用DNN和多個變數進行regression """
normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_features))

  
dnn_model = tf.keras.Sequential([
    normalizer,
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(1)  #output layer
])


#dnn_model.summary()

"配置神經網路模型"
dnn_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='mean_absolute_error'
    )

"對模型進行訓練"
history = dnn_model.fit(
        train_features,
        train_labels,
        epochs=200,
        # logging.
        verbose=2,
        # Calculate validation results on 20% of the training data.
        validation_split = 0.2)

test_results = {}
test_results['dnn_model'] = dnn_model.evaluate(
                            test_features, test_labels, verbose=2)

#畫圖 Loss vs. Epoch
def plot_loss(history):
    plt.figure(figsize=(12,6), dpi=90)
    plt.axes([0.12, 0.16, 0.85, 0.75]) #axes( [x, y, width, height] )
    plt.plot(history.history['loss'], linewidth=3, label='train_loss')
    plt.plot(history.history['val_loss'], linewidth=3, label='val_loss')
    #plt.xlim([0, 150])
    #plt.ylim([0, 15])
    plt.xlabel('Epoch', size=24)
    plt.ylabel('Loss', size=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend()
    plt.grid(True)
    plt.savefig('plot_bike_rental_loss.png')
    
plot_loss(history)


#畫圖 測試集的預測結果 vs. 實際值 
x = tf.linspace(0.0, 3000, 3001)
y = 1.* x

test_prediction = dnn_model.predict(test_features).flatten() #1D-data

def plot_predictions(x, y):
    plt.figure(figsize=(12,6), dpi=90)
    plt.axes([0.12, 0.16, 0.85, 0.75])
    plt.scatter(test_labels, test_prediction, c='g',label='Real')
    
    plt.plot(x, y, color='k', linewidth=3, label='Prediction')
    plt.xlabel('Real', size=24)
    plt.ylabel('Prediction', size=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend()
    plt.savefig('plot_bike_rental_predict.png')

plot_predictions(x, y)


#誤差分布
hist_error = test_prediction - test_labels
plt.figure(figsize=(12,6), dpi=90)
plt.hist(hist_error, bins=80)
plt.xlim([-800, 800])
plt.xlabel('Prediction Error', size=24)
plt.ylabel('Count', size=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.savefig('plot_bike_rental_hist_error.png')


dnn_model.save('dnn_model_rent_bike.keras')
