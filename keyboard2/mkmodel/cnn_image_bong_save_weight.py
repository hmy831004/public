
# coding: utf-8

# In[18]:


from PIL import Image
import os, glob
import numpy as np
from sklearn.model_selection import train_test_split
import random, math


# In[19]:


# 유물 사진 저장되어 있는 디렉토리 
root_dir="/home/ubuntu/tf-demo/Django/mysite/keyboard/mkmodel/um"
# 전체경로: C:/Users/acorn/Dropbox/ChiYH/WorkSpace/final_project/한국사 내용 정리/유물

# 사진 사이즈
image_size=50


# In[21]:


# 분류대상 카테고리 만들기 

# 유물 폴더의 하위 폴더를 이용해서 자동으로 categories 읽어온다 

# 디렉토리 하위 폴더를 모두 읽어 온다
things=glob.glob(root_dir+"/"+"*")

# 카테고리 생성
#categories=['금동대향로','금동연가7년명여래입상','마애여래삼존상']
categories=['금동대향로','금동연가7년명여래입상','마애여래삼존상','반가사유상','부여정림사지5층석탑','불국사3층석탑','사택지적비','산수무늬벽돌','삼한통보','여주고달사지승탑','칠지도']

#for thing in things:
    # 폴더 경로에서 '\\'뒤의 폴더 이름을 카테고리로 지정할 것이다.
    # 폴더 중 연습용 폴더는 필요 없다. 
#    print(thing)
#    cate=thing.split("\\")[1]
#    if cate !='연습용':
#        categories.append(cate)



# In[6]:


# 폴더마다의 이미지 데이터 읽어 들이고 그 이미지의 레이블 만들기

def making_data():
    x=[] # 이미지 데이터
    y=[] # 레이블 데이터
    print(categories)
    for idx, cat in enumerate(categories):
        image_dir=root_dir+"/"+cat
        print(image_dir)
        files=glob.glob(image_dir+"/"+"*.jpg")
        print(files) 
        for i, f in enumerate(files):
            img=Image.open(f)
            img=img.resize((image_size, image_size)) # 이미지 크기 변경
            #print(img)
            data=np.asarray(img)
            #print(data)
            x.append(data)
            y.append(idx)
            
            # 각도를 조금 변경한 파일 추가하기
        
            #회전하기
            for ang in range(-20, 20, 5):
                # -20,-15,-10,-5,0,5,10,15
                img2=img.rotate(ang)
                data=np.asarray(img2)
                x.append(data)
                y.append(idx)
            
                #반전하기
                img2=img2.transpose(Image.FLIP_LEFT_RIGHT)
                data=np.asarray(img2)
                x.append(data)
                y.append(idx)
       
    # 데이터가 담겨 있는 리스트를 ndarray객체로 바꿔준다. 
    # 이유는 각 데이터 값을 0에서 1로 정규화하기 위해서는 numpy의 astype
    # 함수를 써야하는데 이는 ndarray에서만 가능하다. 
    x=np.array(x)
    y=np.array(y)
    
    return x,y


# In[7]:


# 분류 대상 카테고리

nb_classes=len(categories)
print(nb_classes)

# In[9]:


# main - 데이터 훈련시키고 평가
def main():
    
    # 훈련시킬 데이터 만들기
    data=making_data()
    x=data[0] # 이미지 데이터
    y=data[1] # 라벨 indexing 데이터
    
    # 데이터 분류하기
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.25)

    # 정규화 각 필셀 데이터를 256으로 나눠 데이터를 0에서 1의 범위로 정규화
    x_train=x_train.astype("float32")/256
    x_test=x_test.astype("float32")/256
    
    # to_categorical()메소드를 이용하여 class vector(integers)를 binary class matrix로 변환
    y_train=np_utils.to_categorical(y_train, nb_classes)
    y_test=np_utils.to_categorical(y_test, nb_classes)
    
    # 모델 훈력하기
    model=model_train(x_train,y_train)
    
    # 모델 평가하기
    model_eval(model,x_test, y_test)
    
    return model


# In[10]:


# 모델 훈련하기
def model_train(x,y):
    model=build_model(x.shape[1:]) # shape[1:] = (nb_classes,) =(11,)
    model.fit(x,y, batch_size=16, epochs=10)
    
    # 모델 저장하기 
    model.save_weights('model_save_weight')
    #model.save('model_cnn_detail_bt16_nbepoch10_img3')
    return model


# In[11]:


# 모델 평가하기
def model_eval(model, x, y):
    score=model.evaluate(x,y)
    print('loss=', score[0])
    print('accuracy=', score[1])


# In[13]:


# CNN 학습시키기

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, AveragePooling2D, Conv2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np


# In[14]:


# 모델 구축하기

def build_model(in_shape):
    model = Sequential()
    #model.add(Convolution2D(16,3,3, border_mode='same', input_shape=in_shape))
    model.add(Conv2D(16,(3,3), input_shape=in_shape, padding="same"))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    #model.add(Convolution2D(32,3,3,border_mode='same'))
    model.add(Conv2D(32,(3,3), padding="same"))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy',
                 optimizer='rmsprop',
                 metrics=['accuracy'])
    return model


# In[22]:


if __name__ == "__main__":
    main()

