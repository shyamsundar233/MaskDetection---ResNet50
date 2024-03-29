# -*- coding: utf-8 -*-
"""ResNet50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XPPiyAND4ULihREeocecRKUAyHhqNXTS
"""

import tensorflow as tf
from keras.layers import Conv2D,BatchNormalization,Activation,MaxPooling2D,AveragePooling2D
from keras.initializers import glorot_uniform

def identity_block(x,f,filters):
  F1,F2,F3 = filters
  x_temp = x

  #First layer
  x = Conv2D(filters=F1,kernel_size=(1,1),strides=(1,1),padding='valid')(x)
  x = BatchNormalization(axis=3)(x)
  x = Activation('relu')(x)

  #Second layer
  x = Conv2D(filters=F2,kernel_size=(f,f),strides=(1,1),padding='same')(x)
  x = BatchNormalization(axis=3)(x)
  x = Activation('relu')(x)

  #Third layer
  x = Conv2D(filters=F3,kernel_size=(1,1),strides=(1,1),padding='valid')(x)
  x = BatchNormalization(axis=3)(x)

  #Final Step
  x = tf.keras.layers.Add()([x,x_temp])
  x = Activation('relu')(x)

  return x

def convolutional_block(x,f,filters,s=2):
  F1,F2,F3 = filters
  x_temp = x

  #First layer
  x = Conv2D(F1,(1,1),strides=(s,s))(x)
  x = BatchNormalization(axis=3)(x)
  x = Activation('relu')(x)

  #Second layer
  x = Conv2D(filters=F2,kernel_size=(f,f),strides=(1,1),padding='same')(x)
  x = BatchNormalization(axis=3)(x)
  x = Activation('relu')(x)

  #Third layer
  x = Conv2D(filters=F3,kernel_size=(1,1),strides=(1,1),padding='valid')(x)
  x = BatchNormalization(axis=3)(x)

  #Shortcut Layer
  x_temp = Conv2D(filters=F3,kernel_size=(1,1),strides=(s,s),padding='valid')(x_temp)
  x_temp = BatchNormalization(axis=3)(x_temp)

  #Final layer
  x = tf.keras.layers.Add()([x,x_temp])
  x = Activation('relu')(x)
  
  return x

def ResNet50(input_shape=(224,224,3),classes=2):
  
  x_input = tf.keras.layers.Input(input_shape)
  x = tf.keras.layers.ZeroPadding2D((3,3))(x_input)

  #stage 1
  x = Conv2D(64,(7,7),strides=(2,2))(x)
  x = BatchNormalization(axis=3)(x)
  x = Activation('relu')(x)
  x = MaxPooling2D((3,3),strides=(2,2))(x)

  #stage 2
  x = convolutional_block(x,f=3,filters=[64,64,256],s=1)
  x = identity_block(x,3,[64,64,256])
  x = identity_block(x,3,[64,64,256])

  #stage 3
  x = convolutional_block(x,f=3,filters=[128,128,512],s=2)
  x = identity_block(x,3,[128,128,512])
  x = identity_block(x,3,[128,128,512])
  x = identity_block(x,3,[128,128,512])

  #stage 4
  x = convolutional_block(x,f=3,filters=[256,256,1024],s=2)
  x = identity_block(x,3,[256,256,1024])
  x = identity_block(x,3,[256,256,1024])
  x = identity_block(x,3,[256,256,1024])
  x = identity_block(x,3,[256,256,1024])
  x = identity_block(x,3,[256,256,1024])

  #stage 5
  x = convolutional_block(x,f=3,filters=[512,512,2048],s=2)
  x = identity_block(x,3,[512,512,2048])
  x = identity_block(x,3,[512,512,2048])
  
  #AvgPool
  x = AveragePooling2D((2,2),name="avg_pool")(x)

  x = tf.keras.layers.Flatten()(x)
  x = tf.keras.layers.Dense(classes,activation='softmax',name='fc' + str (classes),kernel_initializer=glorot_uniform(seed=0))(x)

  model = tf.keras.Model(inputs = x_input, outputs = x, name = 'ResNet50')

  return model
