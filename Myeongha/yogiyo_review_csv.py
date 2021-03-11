import requests
import pandas as pd

#가게코드
restaurant_code = 338641

#리뷰API주소
url = "https://www.yogiyo.co.kr/api/v1/reviews/"+str(restaurant_code)+"/?only_photo_review=false&sort=time"

data = requests.get(url).json() #api를 json형태로 받아오기
#print(json.dumps(data, indent="\t",ensure_ascii=False)) #JSON출력 결과 확인용

filename = 'review_' + str(restaurant_code) +'.csv' #csv파일명 지정(가게코드로 구분)

print("가게코드 "+str(restaurant_code)+ "의 csv파일명: "+ filename)
df = pd.json_normalize(data)
df.to_csv(filename, encoding='utf-8-sig')

