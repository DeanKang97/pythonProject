from collections import Counter
import pandas as pd  # 판다스

from konlpy.tag import *
from hanspell import spell_checker


def countwords():
    data = pd.read_csv("/Users/deankang/Documents/Github/pythonProject/api_user/reviews.csv")  # 대상 데이터 로딩
    data = data.drop_duplicates(["content"], keep="last")

    data["content"] = data["content"].str.lower()  # 영어는 소문자로 통합
    hp = ''
    for d in data['content']:  # 리뷰 하나의 str로 합
        hp += str(d)

    spelled_sent = spell_checker.check(hp)
    hp += spelled_sent.checked

    okt = Okt()
    noun = okt.nouns(hp)  # 명사로 토큰화

    # 불용어 제거
    stopwords = ['뭐', '으면', '을', '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로',
                 '자', '에', '와', '한', '하다', '.', '👍', '~', '♥', '^^', 'ㅎㅎ', '좋아요', '너무', '!', '피부'
        , '사용', '용량', '구매', '써', '같아요', '솜', '것', '거', '토너', '앰플', '로션', '에센스', '제품', '후', '정리',
                 '때', '더', '스킨']

    arr = []
    for i in range(0, len(noun)):
        if not noun[i] in stopwords:
            arr.append(noun[i])

    count = Counter(arr)

    ans = list()


    for a, b in count.most_common(5):  # 가장 빈도수가 많은 5개 출력
        ans.append(a)

    return ans

countwords()
