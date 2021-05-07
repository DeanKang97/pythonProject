from collections import Counter

import pandas as pd  # 판다스
from konlpy.tag import *
from hanspell import spell_checker

import numpy as np

from nltk import FreqDist
# 실행했을 때 에러 메시지로 punkt에러 나면 밑에 명령어 한번 실행
# nltk.download("punkt")


data = pd.read_csv('../TaeGeun/reviews.csv')  # 대상 데이터 로딩

data = data.drop_duplicates(["content"], keep="last")

data["content"] = data["content"].str.lower()  # 영어는 소문자로 통합

# # 영어를 한글로 변환
# data["리뷰내용"] = data["리뷰내용"].str.replace("iphone", "아이폰") \
#     .str.replace("black", "블랙").str.replace("GB", "기가")

hp = ''
for d in data['content']:  # 리뷰 하나의 str로 합
    hp += str(d)

spelled_sent = spell_checker.check(hp)
hp += spelled_sent.checked

okt = Okt()
print("----------using .morphs--------")

phr = okt.morphs(hp)  # Parse phrase to morphemes
print(phr)

noun = phr
#불용어 제거
stopwords = ['뭐', '으면', '을', '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로',
             '자', '에', '와', '한', '하다','.', '👍', '~', '♥', '^^','ㅎㅎ']

arr = []
for i in range(0,len(noun)):
    if not noun[i] in stopwords:
        arr.append(noun[i])

count = Counter(arr)

for a,b in count.most_common(10):
    print(a)

