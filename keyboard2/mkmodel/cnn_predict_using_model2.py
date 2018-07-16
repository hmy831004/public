
# coding: utf-8

# In[1]:


from PIL import Image
import os, glob
import numpy as np
import requests
from io import BytesIO


# In[3]:


from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, AveragePooling2D, Conv2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np


# In[5]:


# 입력 이미지 변환하기

image_size=50

# 카테고리 생성
categories=['금동대향로','금동연가7년명여래입상','마애여래삼존상','반가사유상','부여정림사지5층석탑','불국사3층석탑','사택지적비','산수무늬벽돌','삼한통보','여주고달사지승탑','칠지도']

x=[]
url=[]
url="http://dn-m.talk.kakao.com/talkm/bl2SlCiJqox/0leS1yd2Uh31W445z6h230/i_daxu63ces3mu1.jpg"

response=requests.get(url)
sample=Image.open(BytesIO(response.content))

sample=sample.resize((image_size, image_size))
sample=np.asarray(sample)
x.append(sample)
x=np.array(x)


# In[9]:


import cnn_image_bong_save_weight as cnn_image

# 모델 구축하기
model = cnn_image.build_model(x.shape[1:])
model.load_weights("model_save_weight")

# CNN 모델 구축하기 
pre=model.predict(x)
#pre=model.predict(x)
print(pre.argmax())
print(categories[pre.argmax()])

