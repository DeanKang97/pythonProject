#!/usr/bin/env python
# coding: utf-8

# In[76]:


import pandas as pd  # 판다스
from konlpy.tag import *
from hanspell import spell_checker

import numpy as np

from nltk import FreqDist
# 실행했을 때 에러 메시지로 punkt에러 나면 밑에 명령어 한번 실행
# nltk.download("punkt")
from collections import Counter


# In[77]:


data = pd.read_csv('fake_review_세라마이드 인텐스 크림.csv')  # 대상 데이터 로딩

data = data.drop_duplicates(["블로그내용"], keep="last")

data["블로그내용"] = data["블로그내용"].str.lower()  # 영어는 소문자로 통합


# In[78]:


hp = ''
for d in data['블로그내용']:  # 리뷰 하나의 str로 합
    hp += str(d)


# In[79]:


spelled_sent = spell_checker.check(hp)
hp += spelled_sent.checked


# In[96]:


okt = Okt()
print("----------using .morphs--------")

phr = okt.morphs(hp)  # Parse phrase to morphemes 형태소 단위 구문 분석 
print(phr)

noun = phr
#불용어 제거
stopwords = ['뭐', '으면', '을', '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다','.']


# In[100]:


arr = []
#불용어 제거
for i in range(0,len(noun)):
    if not noun[i] in stopwords:
        arr.append(noun[i])


# In[101]:


#수동으로 단어 사전들을 만들어서 갯수를 세야함
#화장품이라면 "수부지", "지성" 등 합치고 "건성" "촉촉" 등 합침

vocab = FreqDist(np.hstack(arr))
goodWd = vocab['배송']+vocab['빨리']+vocab['빠름']
badWd = vocab['느려']+vocab['느리고']+vocab['느림']+vocab['늦게']
print('[배송]의 수 '+str(vocab['배송']))
print('[빨리]의 수 '+str(vocab['빨리']))
print('[빠름]의 수 '+str(vocab['빠름']))
print('[빠르게]의 수 '+str(vocab['빠르게']))
print('[느려]의 수 '+str(vocab['느려']))
print('[느리고]의 수 '+str(vocab['느리고']))
print('[늦게]의 수 '+str(vocab['늦게']))
print('[개통]의 수 '+str(vocab['개통']))
print("keyword:")
 #어느쪽이 더 우세한지 출력
if goodWd > badWd:
    print("배송 빠름")
else:
    print("배송 느림")
    

# In[102]:


get_noun = okt.nouns(hp) #블로그 내용 중 명사만 추출
count_noun = Counter(get_noun)

noun_list = count_noun.most_common(100) #가장 많이 나타나는 명사 순으로 100개 저장
for v in noun_list:
    print(v)


# In[107]:


link_count = 0 
contents = []

# \n 지우기 + 링크 개수 카운트
for i in arr:
    if not "\n" in i:  # \n 지우기
        contents.append(i)
    if "www." in i: #링크 개수 카운트
        link_count = link_count+1
print("링크 카운트: " + str(link_count)+"\n")

print(contents)


# In[ ]:




