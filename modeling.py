#imports
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, LSTM
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
train = pd.read_csv('charts/train.csv')

#Collect X images and standardize
train_image = []
best_list = []
for i in range(len(train)):
    if list(train.best)[i] == 1:
        folder = 'best_sellers_images'
        best_list.append(1)
    else:
        folder = 'non_best_sellers_images'
        best_list.append(0)
    img = image.load_img(folder+'/'+list(train.image)[i], target_size=(128,128,3), grayscale=False)
    img = image.img_to_array(img)
    #standardize
    img = img/255
    train_image.append(img)
X = np.array(train_image)
y_ = np.array(best_list)
y = to_categorical(y_)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Building CNN for RGB
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(128,128,3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])

#train
model.fit(X_train, y_train, epochs=4, validation_data=(X_test, y_test))

#save the model
model.save('cover_image.h5')

def singleImgTest(image_path):
    img = image.load_img(target, target_size=(128,128,3), grayscale=False)
    img = image.img_to_array(img)
    img = img/255
    return model.predict(np.array([img]))

#Score
scoreList = model.predict(X)
goodScore = []
for score in scoreList:
    goodScore.append(score[1])
train['score'] = goodScore

confusion = tf.math.confusion_matrix(labels=list(train.best), predictions=list(round(train['score'])), num_classes=2)
seaborn.heatmap(confusion.numpy(), annot=True, fmt="d")