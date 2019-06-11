
# coding: utf-8

# In[1]:


import librosa
from librosa import display

import os
import pandas as pd
from math import log
import keras
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D
init_g = tf.global_variables_initializer()
init_l = tf.local_variables_initializer()
tsession=0
with tf.Session() as sess:
    tfsession=sess
    sess.run(init_g)
    sess.run(init_l)

# In[10]:


def analyseaudio(filename):
    model = Sequential()

    model.add(Conv1D(128, 5,padding='same',
                    input_shape=(40,1)))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(MaxPooling1D(pool_size=(8)))
    model.add(Conv1D(128, 5,padding='same',))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Flatten())
    model.add(Dense(8))
    model.add(Activation('softmax'))
    opt = keras.optimizers.rmsprop(lr=0.00005, rho=0.9, epsilon=None, decay=0.0)


    model.load_weights("./mlfiles/model.hdf5")

    X1, sample_rat = librosa.load(filename, res_type='kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=X1, sr=sample_rat, n_mfcc=40).T,axis=0)
    arr1 = mfccs

    x_train = np.expand_dims(arr1, axis=2)
    t=np.array([x_train])

    f=model.predict(t)


    output=model.predict_proba(t)
    output.reshape(-1,1)
    output[0][1]=output[0][0]+output[0][1]
    ot=output[0]
    idx=[3,5,4,1,2,6,0]
    vprobs=ot[1:].reshape(-1,1)[idx]

    summary_writer = tf.summary.FileWriter('./tflogs', sess.graph_def)
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    k=np.array([log(x+1) for x in vprobs])
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler()
    scaler.fit(k.reshape(-1,1))
    t=scaler.transform(k.reshape(-1,1))
    return t

