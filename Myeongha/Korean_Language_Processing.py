
import pandas as pd  # 판다스
from konlpy.tag import *
from hanspell import spell_checker
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
# 실행했을 때 에러 메시지로 punkt에러 나면 밑에 명령어 한번 실행

# nltk.download("punkt")


data = pd.read_csv('reviews.csv')  # 대상 데이터 로딩

data =data.drop_duplicates(["리뷰내용"], keep="last")

data["리뷰내용"] = data["리뷰내용"].str.lower() #영어는 소문자로 통합

#영어를 한글로 변환
data["리뷰내용"] = data["리뷰내용"].str.replace("iphone", "아이폰")\
    .str.replace("black", "블랙").str.replace("GB", "기가")




hp = ''
for d in data['리뷰내용']: # 리뷰 하나의 str로 합
    hp += str(d)

spelled_sent = spell_checker.check(hp)
hp += spelled_sent.checked

okt = Okt()
print("----------using .morphs--------")
phr = okt.morphs(hp) #Parse phrase to morphemes

print(phr)
phr1 = okt.normalize(hp)
print("------------using .normalize-------")
print(phr1)

noun = phr

for a, b in enumerate(noun):
    if len(b) <2: #이 아 가 같은 조사는 생략
        noun.pop(a)


cnt = Counter(noun)

li = cnt.most_common(50)

for i in li:
    print(i)
