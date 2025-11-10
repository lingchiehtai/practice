# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:51:19 2024

@author: Linda
classification for Rock-Paper-Scissors Images dataset 
   1. 資料載入：讀取圖片資料集，將資料轉換為模型可用的格式，以供訓練與驗證。

   2. 訓練模型：使用 TensorFlow/Keras 建立一個卷積神經網路(CNN)模型，進行訓練，使其能夠辨識圖片中的三種手勢。

   3. 評估與預測：訓練完成後，將準確率 (Accuracy) 與損失 (Loss)
      的變化過程繪製成圖表。最後，載入訓練好的模型來預測新圖片的類別。
"""



import pandas as pd
import matplotlib.pyplot as plt
import os
import random
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile
import csv

#============================================
#讀取圖片檔名和label(=分類子資料夾)

dataset_path = './rps-cv-images/'

images = []
labels = []

# Loop over the subfolders in the dataset
for subfolder in os.listdir(dataset_path):
    print(subfolder)
    subfolder_path = os.path.join(dataset_path, subfolder)
    if not os.path.isdir(subfolder_path):
        continue
    # Loop over the images in the subfolder
    for image_filename in os.listdir(subfolder_path):
        image_path = os.path.join(subfolder_path, image_filename)
        images.append(image_path)
        labels.append(subfolder)
        
df = pd.DataFrame({'image': images, 'label': labels})

#============================================
#顯示圖片 每個分類顯示前4張
from matplotlib.gridspec import GridSpec

# Create figure and grid of subplots
fig = plt.figure(figsize=(15, 15))
gs = GridSpec(5, 4, figure=fig)

# Loop through each unique category in the DataFrame
for i, category in enumerate(df['label'].unique()):
    filepaths = df[df['label'] == category]['image'].values[:4]
    for j, filepath in enumerate(filepaths):
        ax = fig.add_subplot(gs[i, j])
        ax.imshow(plt.imread(filepath))
        ax.axis('off')
    ax.text(300, 100, category, fontsize=25, color='darkblue')
plt.show()

#============================================
#原始圖片數量
print(len(os.listdir('./rps-cv-images/paper')))
print(len(os.listdir('./rps-cv-images/rock')))
print(len(os.listdir('./rps-cv-images/scissors')))

"create dir"
# try:
#     os.mkdir('./tmp/paper-rock-scissors')
#     os.mkdir('./tmp/paper-rock-scissors/training')
#     os.mkdir('./tmp/paper-rock-scissors/testing')
#     os.mkdir('./tmp/paper-rock-scissors/training/paper')
#     os.mkdir('./tmp/paper-rock-scissors/training/rock')
#     os.mkdir('./tmp/paper-rock-scissors/training/scissors')
#     os.mkdir('./tmp/paper-rock-scissors/testing/paper')
#     os.mkdir('./tmp/paper-rock-scissors/testing/rock')
#     os.mkdir('./tmp/paper-rock-scissors/testing/scissors')
#     print('mkdir: OK!')
# except OSError:
#     pass

#============================================
"原始圖片依照比例複製到training/testing 資料夾"
# def split_data(SOURCE, TRAINING, TESTING, SPLIT_SIZE):
#     files = []
#     for filename in os.listdir(SOURCE):
#         filepath = SOURCE + filename
#         if os.path.getsize(filepath) > 0:  #file size(bytes) 
#             files.append(filename)
#         else:
#             print(filename + " is zero length, so ignoring.")

#     training_length = int(len(files) * SPLIT_SIZE)
#     testing_length = int(len(files) - training_length)
#     shuffled_set = random.sample(files, len(files)) #將檔案列表(files)中的元素進行隨機重排
#     training_set = shuffled_set[0:training_length]
#     testing_set = shuffled_set[-testing_length:]


#     for filename in training_set:
#         this_file = SOURCE + filename
#         destination = TRAINING + filename
#         copyfile(this_file, destination)

#     for filename in testing_set:
#         this_file = SOURCE + filename
#         destination = TESTING + filename
#         copyfile(this_file, destination)


# img1_SOURCE_DIR = "./rps-cv-images/paper/"
# TRAINING_img1_DIR = "./tmp/paper-rock-scissors/training/paper/"
# TESTING_img1_DIR = "./tmp/paper-rock-scissors/testing/paper/"
# img2_SOURCE_DIR = "./rps-cv-images/rock/"
# TRAINING_img2_DIR = "./tmp/paper-rock-scissors/training/rock/"
# TESTING_img2_DIR = "./tmp/paper-rock-scissors/testing/rock/"
# img3_SOURCE_DIR = "./rps-cv-images/scissors/"
# TRAINING_img3_DIR = "./tmp/paper-rock-scissors/training/scissors/"
# TESTING_img3_DIR = "./tmp/paper-rock-scissors/testing/scissors/"

# split_size = 0.85
# split_data(img1_SOURCE_DIR, TRAINING_img1_DIR, TESTING_img1_DIR, split_size)
# split_data(img2_SOURCE_DIR, TRAINING_img2_DIR, TESTING_img2_DIR, split_size)
# split_data(img3_SOURCE_DIR, TRAINING_img3_DIR, TESTING_img3_DIR, split_size)


#============================================

model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(shape=(150, 150, 3)),  #input_shape修改成這行
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='softmax') # 3元分類
])
#prints a summary of the NN
model.summary()

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


TRAINING_DIR = "./tmp/paper-rock-scissors/training/"
train_datagen = ImageDataGenerator(rescale=1.0/255.)

train_generator = train_datagen.flow_from_directory(TRAINING_DIR,
                                                    batch_size=50,
                                                    class_mode='categorical',
                                                    target_size=(150, 150))

VALIDATION_DIR = "./tmp/paper-rock-scissors/testing/"
validation_datagen = ImageDataGenerator(rescale=1.0/255.)
validation_generator = validation_datagen.flow_from_directory(VALIDATION_DIR,
                                                            batch_size=20,
                                                            class_mode='categorical',
                                                            target_size=(150, 150))

# Save best model
keras_model_name = './best_model.keras'
callbacks = tf.keras.callbacks.ModelCheckpoint(filepath=keras_model_name, 
                                               verbose=2, 
                                               save_best_only=True, 
                                               monitor='val_accuracy',
                                               #monitor='accuracy',
                                               mode='max')

history = model.fit(train_generator, 
                    epochs=20,  #steps_per_epoch=88,
                    validation_data=validation_generator,
                    callbacks=[callbacks],
                   #validation_steps=10)
                   verbose=2)
                   

model.save(keras_model_name)
print("Model saved succesfully!")

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

  
#------------------------------------------------
#write to csv file
with open('accuracy_loss_history.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['epochs', 'acc', 'loss', 'val_acc', 'val_loss'])
    for i in range(len(epochs)):
        writer.writerow([epochs[i], acc[i], loss[i], val_acc[i], val_loss[i]]) 

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.figure(dpi=120)
plt.plot(epochs, acc, 'r', marker='o', label="Training Accuracy")
plt.plot(epochs, val_acc, 'b', marker='o', label="Validation Accuracy")
plt.ylim(0.5, 1)
plt.title('Accuracy')
plt.legend(loc = 'best')
plt.savefig('Accuracy.png') 
#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.figure(dpi=120)
plt.plot(epochs, loss, 'r', marker='o', label="Training Loss")
plt.plot(epochs, val_loss, 'b', marker='o', label="Validation Loss")
plt.ylim(0,1)
plt.title('Loss')
plt.legend(loc = 'best')
plt.savefig('Loss.png') 

#------------------------------------------------
#reload the trained model
#------------------------------------------------
reload_model = tf.keras.models.load_model(keras_model_name)

reload_model.summary()

#reload_model.evaluate(validation_generator)

#------------------------------------------------
#讀取資料夾裡面的圖檔:predict
from keras.preprocessing import image
import numpy as np

c1, c2, c3 = 0, 0, 0
totalNum = 0 

dir_name = './tmp/test-paper/'
#dir_name = './tmp/test-rock/'
#dir_name = './tmp/test-scissors/'
for filename in os.listdir(dir_name):

    # predicting other images
    path = dir_name + filename
    img = image.load_img(path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    
    classes = reload_model.predict(images, batch_size=1)
    a, b, c = classes[0]
    print(classes[0])
    totalNum += 1
    if a>0.9:
        c1 += 1
        print(filename + " is paper.")
    if b>0.9:
        c2 += 1
        print(filename + " is a rock.")
    if c>0.9:
        c3 += 1
        print(filename + " is scissors.")

print('dir name: ',dir_name)
print(f'paper:{c1}/{totalNum}, \nrock:{c2}/{totalNum}, \nscissors:{c3}/{totalNum}')


