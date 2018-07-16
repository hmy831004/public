from gensim.models import Word2Vec
import regex
import numpy as np
from pandas import DataFrame, read_csv

model = Word2Vec.load('/home/ubuntu/tf-demo/Django/mysite/keyboard/model/model_sample')
df0 = read_csv('/home/ubuntu/tf-demo/Django/mysite/keyboard/model/raw_txt/wiki_BJwang3.csv', encoding='cp949')
li_ref = list(map(lambda s: s + ' ' if type(s) == str else '', list(df0['text_ref'])))
str_ref = ''.join(li_ref)
n_ref = list(set(str_ref.split(' ')))

# tr = df0['text_ref'][0].split(' ')  # 단어로 이루어진 문장 // 테스트용

# r which
def mf_idx(TF_):
    res = [i for i, T in enumerate(list(TF_)) if T]
    return res

def mf_W2Vtb(qw_):
    ms = model.wv.most_similar(positive=[qw_], topn=20)
    tb = [[qw_, 1]] + list(map(lambda s: [s[0], s[1]], ms))
    return(tb)
# mf_W2Vtb('시조')  # '시조'의 W2V 단어 유사도

def mf_W2Vsc(qw_, text_ref_):
    score = list(map(lambda s: s[1] if s[0] in text_ref_ else 0, mf_W2Vtb(qw_)))
    score = np.array(score).sum()
    return(score)
# mf_W2Vsc('시조', tr)  # 문장과 '시조'의 유사도 합

def mf_W2Vqs(q_ref_, text_ref_):
    # q_ref = mf_gid(query_, n_ref, 'li')
    score = list(map(lambda s: mf_W2Vsc(s, text_ref_) if type(s) == str else 0, q_ref_))
    score = np.array(score).sum()
    return (score)
# mf_W2Vqs(['백제','시조'], tr)  # 한 문장에 포함된 전체 단어에 대한 스코어

def mf_gnr(pattern_, string_):
    if regex.search(pattern_, string_):
        return([pattern_, regex.search(pattern_, string_).start()])
    return([None, None])
# mf_gnr('시조', '백제의 시조는 누구일까?')  # 문장 내의 단어와 위치를 반환

def mf_gid(string_, dic_, option_ = 'li'):
    tmp_li = np.array(list(map(lambda s: mf_gnr(s, ' ' + string_), dic_)))
    tmp_df = DataFrame(tmp_li[mf_idx(tmp_li[:, 1])])
    tmp_df = tmp_df.sort_values(1)
    if option_ == 'li':
        return (list(tmp_df.iloc[:,0]))
    if option_ == 'str':
        return (' '.join(list(tmp_df.iloc[:,0])))
# mf_gid(li_t[0], n_ref, 'str')  # 문장에서 사전에 있는 단어만 추출하여 리스트 또는 텍스트로 반환

def mf_bjW2V(query_):
    # score = list(map(lambda s: diff_ngram(query_, str(s), 3), list(df.text_ref)))
    q_ref_ = mf_gid(query_, n_ref, 'li')
    score = list(map(lambda s: mf_W2Vqs(q_ref_, s) if type(s) == str else 0, list(df0.text_ref)))

    df0['score'] = score
    return('query :'+str( query_)+
          '\nwang :'+str( list(df0.loc[df0.score == max(score)].wang))+
          '\ntext :'+str( list(df0.loc[df0.score == max(score)].text)))
	
    
 #   return(df0.loc[df0.score == max(score)])

#print(mf_bjW2V('백제의 전성기'))



