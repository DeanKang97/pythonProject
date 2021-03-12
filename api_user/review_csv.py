import requests
import pandas as pd
import csv


class reviewInfo:
    comment = 'comment'
    rating = 5
    menu = "fried chicken"
    time = "2021-09-18"

    def __init__(self, comment, rating, menu, time):
        self.comment = comment
        self.rating = rating
        self.menu = menu
        self.time = time


def getcomments(restaurant_code):
    # restaurant_code = 338641
    url = "https://www.yogiyo.co.kr/api/v1/reviews/" + str(restaurant_code) + "/?only_photo_review=false&sort=time"

    data = requests.get(url).json()  # api를 json형태로 받아오기
    # print(json.dumps(data, indent="\t",ensure_ascii=False)) #JSON출력 결과 확인용

    filename = 'review_' + str(restaurant_code) + '.csv'  # csv파일명 지정(가게코드로 구분)

    print("가게코드 " + str(restaurant_code) + "의 csv파일명: " + filename)
    df = pd.json_normalize(data)
    df.to_csv(filename, encoding='utf-8-sig')

    exelfile = open("review_" + str(restaurant_code) + ".csv")
    headers = csv.reader(exelfile)
    summary = list()

    for i in headers:
        summary.append(reviewInfo(i[1], i[2], i[7], i[16]))

    for j in summary:
        print(j.menu)

    summary.pop(0)

    # headers[1] -> comment
    # headers[2] -> rating
    # headers[7] -> menu
    # headers[16] -> time
    return summary


getcomments(338641)
