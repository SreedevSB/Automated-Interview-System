
# coding: utf-8

# In[12]:


import numpy as np
from matplotlib import pyplot as plt
import os
'''
from keras.layers import Dense, Convolution2D, UpSampling2D, MaxPooling2D, ZeroPadding2D, Flatten, Dropout, Reshape
from keras.models import Sequential,load_model
from keras.utils import np_utils
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
'''
from keras.models import load_model
from keras import backend as K
from keras.preprocessing import image
#K.set_image_dim_ordering('th')
from pathlib import Path



import tensorflow as tf
import keras
#cpu - gpu configuration
config = tf.ConfigProto( device_count = {'GPU': 30 , 'CPU': 56} ) #max: 1 gpu, 56 cpu
sess = tf.Session(config=config) 
K.set_session(sess)
graph = sess.graph
tfsession=0

init_g = tf.global_variables_initializer()
init_l = tf.local_variables_initializer()
with tf.Session() as sess:
    tfsession=sess
    sess.run(init_g)
    sess.run(init_l)
# In[13]:

import cv2
import math
import logging as log
import datetime as dt
import time

def getFaceFrame(image):

    cascPath = "./mlfiles/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    frame = image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),

    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (x,y,w,h) in faces:
        detected_face = frame[int(y):int(y+h), int(x):int(x+w)] #crop detected face
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
        detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
        #filename ="pics/test%d.jpg" % count;
        #cv2.imwrite(filename, detected_face)
        
        return detected_face

    #print ("Done!")

def emotion_analysis(emotions):
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, emotions, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)

    plt.ylabel('percentage')
    plt.title('emotion')
    
    #plt.show()
def swish_activation(x):
    return (K.sigmoid(x) * x)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])



# In[27]:


model=load_model("./mlfiles/final (1).h5",custom_objects={'swish_activation': swish_activation})
graph = tf.get_default_graph() 


def analysevideo(filename):
    emotions=list()   
    cap = cv2.VideoCapture(filename)
    global model
    global graph
    counter=0
    
    with graph.as_default():
        while(cap.isOpened()):
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                # If the number of captured frames is equal to the total number of frames,
                # we stop
                break
                
            frameId = cap.get(1) #current frame number
            ret, frame = cap.read()

            if (ret != True):
                break
                
            #videogen = skvideo.io.vreader()
            #for frame in videogen:   
            #print(frame)
            #img=image.load_img(frame, color_mode = "grayscale", target_size=(48, 48))
            #x = image.img_to_array(img)
            
            from PIL import Image
            #x = rgb2gray(frame)
            #im = Image.fromarray(x)
            

            k=getFaceFrame(frame)
            filename ="./mlfiles/facepics/test%d.jpg" % counter;
            
            if(cv2.imwrite(filename, k)):
            
                #k = Image.fromarray(k)
                my_file = Path(filename)
                if not my_file.is_file():
                    continue
                img=image.load_img(filename, color_mode = "grayscale", target_size=(48, 48))
                k = image.img_to_array(k).reshape(1,48,48)
                #print(k)

                if k is None:
                    continue

                k = np.expand_dims(k, axis = 0)
                k/=255

                custom = model.predict(k)
                emotions.append(custom[0])


                #emotion_analysis(custom[0])

                x = np.array(k, 'float32')
                x = x.reshape([48, 48]);
                counter+=1
                #plt.gray();plt.imshow(x);plt.show()   
    #print ("emotions") 
    #print(len(emotions))
    esum=[0,0,0,0,0,0,0]
    for e in emotions:
        esum=np.add(e,esum)
    #print ("esum")
    #print(esum)

    #summary_writer = tf.summary.FileWriter('./tflogs', sess.graph_def)
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler()
    scaler.fit(esum.reshape(-1,1))
    t=scaler.transform(esum.reshape(-1,1))
    #print(objects[esum.argmax()])
    #emotion_analysis(esum)
    return t
