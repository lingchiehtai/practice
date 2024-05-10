# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:13:59 2024

@author: Linda
Iris image classification
https://ithelp.ithome.com.tw/articles/10321099
"""

from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical

#載入鳶尾花分類數據集
dataset = datasets.load_iris()

x = dataset.data
y = dataset.target

#對Y進行one-hot編碼，one-hot編碼是將每個類別映射為一個向量，其中只有一個元素為 1（表示該樣本屬於該類別），其他元素都為 0。
y = to_categorical(y)  
tr_x, te_x, tr_y, te_y = train_test_split(x, y, train_size=0.8)


#建立基本的神經網路
model = Sequential()
model.add(Input(shape=(4,)))
model.add(Dense(units=4, activation='relu', kernel_initializer='glorot_uniform'))
model.add(Dense(units=6, activation='relu', kernel_initializer='glorot_uniform'))
model.add(Dense(units=3, activation='softmax', kernel_initializer='glorot_uniform'))
model.summary()

#編譯模型時 使用了Adam作為優化器，損失函數為categorical_crossentropy(分類交叉熵)，並以accuracy(準確率)作為評估指標
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


#使用model.fit來訓練模型
history = model.fit(tr_x, tr_y, batch_size=16, epochs=300)

acc=history.history['accuracy']
loss=history.history['loss']

#評估模型在訓練集和測試集上的表現
train_loss, train_accuracy = model.evaluate(tr_x, tr_y)
print('Train Loss:', train_loss)
print('Train Accuracy:', train_accuracy)

test_loss, test_accuracy = model.evaluate(te_x, te_y)
print('Test Loss:', test_loss)
print('Test Accuracy:', test_accuracy)

#預測測試集並列出預測結果

predictions = model.predict(te_x, batch_size=1)

num=0
for i in range(len(predictions)):
    
    predicted_class = np.argmax(predictions[i])  #最大值的索引值
    actual_class = np.argmax(te_y[i])
    print(f'Sample {i+1}: Predicted class = {predicted_class}, Actual class = {actual_class}')
    if predicted_class == actual_class:
        num +=1
    
print('accuracy:' , num/len(predictions))