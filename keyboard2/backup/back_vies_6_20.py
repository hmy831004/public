from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from konlpy.tag import *
from konlpy.jvm import init_jvm
import jpype

#6월 20일 한국어 처리해서 장고에서 왕이름만 뽑아내는 것 까지 성공한 소스



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
#초기 카카오 페이지 띄워 주는 함수
def keyboard(request):


	return JsonResponse({
        	'type' : 'text',
        	#'buttons' : ['고의왕', '유물', '업적', '활동시기']
   	 })


@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	

	dbs = getDB()
	#딕셔너리 선언
	kor = {}
	#디비에 있는 정보들을 가져와서 하나의 딕셔너리로 통합 해주는 작업
	for j in dbs.find():
		texts=j['이름']
		kor[j['이름']]=j
		kor[j['이름']].pop('_id')	
	
	keyword=getKonlp(return_str)
	word=[x for x in keyword if x in kor.keys()]
	word="".join(word)
	if word =="":
		text='keyword 가 존재하지 않습니다.'
	else:
		text=str(kor[word])
	#text=return_str
	return JsonResponse({
                'message': {
                        'text': text
                }
		#,
                #'keyboard': {
                #        'type': 'buttons',
                #        'buttons' : ['고의왕', '유물', '업적', '활동시기']
                #}
        })






