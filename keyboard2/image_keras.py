from PIL import Image
import os, glob
import numpy as np
import requests
from io import BytesIO
import tensorflow as tf
# model 가져오기
from keras.models import load_model
from keras import backend as K
import os
import gc
import sys
sys.path.append('/home/ubuntu/tf-demo/Django/mysite/keyboard/mkmodel')
import cnn_image_bong_save_weight as cnn_image
from pymongo import MongoClient
def match_image(url):
	
	try:


		image_size=50
		categories=['금동대향로','금동연가7년명여래입상','마애여래삼존상','금동미륵보살반가사유상','정림사지5층석탑','불국사3층석탑','사택지적비','산수무늬벽돌','삼한통보','여주고달사지승탑','칠지도']
		#categories=["금동대향로","사택지적비","산수무늬벽돌","마애여래삼존상","칠지도"]

		x=[]

		response=requests.get(url)
		sample=Image.open(BytesIO(response.content))

		sample=sample.resize((image_size, image_size))
		sample=np.asarray(sample)
		x.append(sample)
		x=np.array(x)

		response =requests.delete(url)
		# CNN 모델 구축하기 
		K.clear_session()
		model = cnn_image.build_model(x.shape[1:])
		model.load_weights("/home/ubuntu/tf-demo/Django/mysite/keyboard/mkmodel/model_save_weight")

		pre=None
		pre=model.predict(x)
		kor={}
		dbs=getDB()
		for j in dbs.find():
			kor[j['이름']]=j
			kor[j['이름']].pop('_id')		
			kor[j['이름']].pop('이름')
		item_list=[]
		key=""
		#all_data 함수에서 kor에 저장된 정보를 모두 가져와서 item_list에다가 저장한다.
		all_data(kor[categories[pre.argmax()]],key,item_list)
		text=categories[pre.argmax()]+"\n\n"+"\n".join(item_list)
		return text 
		#return categories[pre.argmax()]

	except Exception as ex:
		return 'errors = '+str(ex)

def getDB():
	client = MongoClient('localhost',27017)
	db = client['kor_hist']
	doc= db['um']
	return doc

def all_data(kors,key,item_list):
	if type(kors)==dict:
		for k in kors:
			key=k
			all_data(kors[k],key,item_list)
	else:
		item_list.append("·"+str(key)+" : "+str(kors))
		return str(kors)


if __name__ == "__main__":
	print("tt")
