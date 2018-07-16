from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from konlpy.tag import *
from konlpy.jvm import init_jvm
import jpype
from urllib import request, parse
import json


i=0;king_flag="";keyword_flag="";user_text=[]
#DB와의 커넥션을 얻기 위해서 사용 하는 함수
def getDB():

	client = MongoClient('localhost',27017)
	db = client['kor_hist']
	doc= db['people_kings']
	return doc

#사용자가 질문한거 konlpy 돌렸을 때 숫자들 제거하기 위한 함수
def is_not_number(num):
    try:
        float(num)
        return(False)
    except:
        return(True)

#사용자가 입력한 문장을 NLP 처리하여 키워드 추출하는 함수
def getKonlp(text):
	

	if jpype.isJVMStarted():
		jpype.attachThreadToJVM()
	han =None
	han = Hannanum()
	keyword=han.nouns(text)
	
	return list(filter(is_not_number,keyword))

#딕셔너리에 키 값이 주어지면 그 딕셔너리를 반환해준다.
def _finditem(obj, key):
	if key in obj: return obj[key]
	for k, v in obj.items():
		if isinstance(v,dict):
			item = _finditem(v, key)
			if item is not None:
                		return item



#딕셔너리 안에 존재하는 모든 키값과 밸류값을 마지막 까지 접근해서 모두 가져 온다.
#recursive 사용해서 구현
def all_data(kors,key,item_list):
	if type(kors)==dict:
		for k in kors:
			key=k
			all_data(kors[k],key,item_list)
	else:
		item_list.append("·"+str(key)+" : "+str(kors))
		return str(kors)


def send_request():
	datas={"user_key": "encryptedUserKey",
	  "type": "text",
	  "content": "차량번호등록"
	}
	data = json.dumps(datas)
	data = str(data)
	data = data.encode('utf-8')
	req =  request.Request('http://13.209.5.82:8001/message', data=data)
	resp = request.urlopen(req)

#초기 카카오 페이지 띄워 주는 함수
def keyboard(request):

	return JsonResponse({
        	#'type' : 'text',
		'type':'buttons',
		'buttons':['roll','lang']
   	 })


def message(return_str):

	
	#message = ((request.body).decode('utf-8'))
	#return_json_str = json.loads(message)
	#return_str = return_json_str['content']
	#user_key = return_json_str['user_key']	


	'''	text=""
	global i,king_flag,keyword_flag,user_text

	
	mongo_key_list=['활동시기','업적','이름','모든정보']
	dbs = getDB()
	#딕셔너리 선언
	kor = {}
	#디비에 있는 정보들을 가져와서 하나의 딕셔너리로 통합 해주는 작업
	for j in dbs.find():
		texts=j['이름']
		kor[j['이름']]=j
		kor[j['이름']].pop('_id')	
	
	keyword=getKonlp(return_str)
	
	#king_word는 keyword 안에서 왕의 이름을 가지고 있는 word 가 있는지를 담는 변수이다.
	king_word=[x for x in keyword if x in kor.keys()]
	king_word="".join(king_word)
	
	if king_word!="":king_flag=king_word
	#몽고 디비안에 있는 키워들들이 유저가 입력한 단어들에 포함되어 있는지 확인하는 작업.
	mongo_keyword=[z for z in keyword if z in mongo_key_list]
	mongo_keyword="".join(mongo_keyword)
	if mongo_keyword !="":
		keyword_flag=mongo_keyword


	#보유하고 있는 왕에대한 질문이 들어왔는지 , 질문이 들어 왔다면 어떤걸 묻고 있는지
	#flag를 사용해서 확인하고 들어가서 내부적으로 수행한다.
	add={}
	if king_flag == "" and keyword_flag=="":
		text="이러한 왕들의 리스트를 가지고 있습니다.\n 어떤 왕을 알고싶으십니까?\n"
		text =text+ '\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(kor.keys())])
		text=text
	elif king_flag!="" and keyword_flag=="":
		text= king_flag+"의 어떠한 것을 알고 싶습니까.\n"
		text = text+'\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(mongo_key_list)])
		
	elif king_flag=="" and keyword_flag!="":
		text="어떤왕이 했던 업적이 궁금하신 겁니까\n"
		text =text+ '\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(kor.keys())])
	elif king_flag!="" and keyword_flag!="":
		text=king_flag+"의 "+keyword_flag+"을 알려 드리겠습니다.\n"

		if keyword_flag=='업적':
			item_list=[]
			key=""
			all_data(_finditem(kor[king_flag],'업적'),key,item_list)
			text = '\n'.join(item_list)
		elif keyword_flag=='활동시기':
			text = text+str(kor[king_flag]['활동시기']+"\n")		
			text = text+keyword_flag
		
		elif keyword_flag=='이름':
			text = text+str(kor[king_flag]['이름']+'\n')

		elif keyword_flag=='모든정보':

			item_list=[]
			key=""
			all_data(kor[king_flag],key,item_list)
		
			text='\n'.join(item_list)

		add={
			'label':king_flag+"을 더알기",
			'url':'https://ko.wikipedia.org/wiki/'+king_flag
		}	
		king_flag=""
		keyword_flag=""
	'''
	
	text="ch"
	add={}
	(text2,add2)=roll(return_str)
	
	if len(add)==0:
		return 1
		'''return JsonResponse({
                	'message': {
                       		'text': text,
              
			 },
			#'keyboard':{
			#'type':'buttons',
			#'buttons':["text","teq"]
			
			#}
        	})'''

	else :
		return 0
		'''return JsonResponse({
			'message': {
        	                'text': text,
              
				'message_button':add
		  	}
       		 })'''




def roll(return_str):

	text=""
	global i,king_flag,keyword_flag,user_text

	
	mongo_key_list=['활동시기','업적','이름','모든정보']
	dbs = getDB()
	#딕셔너리 선언
	kor = {}
	#디비에 있는 정보들을 가져와서 하나의 딕셔너리로 통합 해주는 작업
	for j in dbs.find():
		texts=j['이름']
		kor[j['이름']]=j
		kor[j['이름']].pop('_id')	
	
	keyword=getKonlp(return_str)
	
	#king_word는 keyword 안에서 왕의 이름을 가지고 있는 word 가 있는지를 담는 변수이다.
	king_word=[x for x in keyword if x in kor.keys()]
	king_word="".join(king_word)
	
	if king_word!="":king_flag=king_word
	#몽고 디비안에 있는 키워들들이 유저가 입력한 단어들에 포함되어 있는지 확인하는 작업.
	mongo_keyword=[z for z in keyword if z in mongo_key_list]
	mongo_keyword="".join(mongo_keyword)
	if mongo_keyword !="":
		keyword_flag=mongo_keyword


	#보유하고 있는 왕에대한 질문이 들어왔는지 , 질문이 들어 왔다면 어떤걸 묻고 있는지
	#flag를 사용해서 확인하고 들어가서 내부적으로 수행한다.
	add={}
	if king_flag == "" and keyword_flag=="":
		text="이러한 왕들의 리스트를 가지고 있습니다.\n 어떤 왕을 알고싶으십니까?\n"
		text =text+ '\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(kor.keys())])
		text=text
	elif king_flag!="" and keyword_flag=="":
		text= king_flag+"의 어떠한 것을 알고 싶습니까.\n"
		text = text+'\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(mongo_key_list)])
		
	elif king_flag=="" and keyword_flag!="":
		text="어떤왕이 했던 업적이 궁금하신 겁니까\n"
		text =text+ '\n'.join([str(x[0]+1)+"."+str(x[1]) for x in enumerate(kor.keys())])
	elif king_flag!="" and keyword_flag!="":
		text=king_flag+"의 "+keyword_flag+"을 알려 드리겠습니다.\n"

		if keyword_flag=='업적':
			item_list=[]
			key=""
			all_data(_finditem(kor[king_flag],'업적'),key,item_list)
			text = '\n'.join(item_list)
		elif keyword_flag=='활동시기':
			text = text+str(kor[king_flag]['활동시기']+"\n")		
			text = text+keyword_flag
		
		elif keyword_flag=='이름':
			text = text+str(kor[king_flag]['이름']+'\n')

		elif keyword_flag=='모든정보':

			item_list=[]
			key=""
			all_data(kor[king_flag],key,item_list)
		
			text='\n'.join(item_list)

		add={
			'label':king_flag+"을 더알기",
			'url':'https://ko.wikipedia.org/wiki/'+king_flag
		}	
		king_flag=""
		keyword_flag=""


	return (text,add)


print(message("roll"))
