import requests

url = "https://openapi.naver.com/v1/search/blog?query="  # 네이버 검색 api

client_id = "iq6LEjpJhnsJLV5ev7_a"
client_key = "XZIPTU2d03"

header = {"X-Naver-Client-Id": client_id,  # api_key and id
          "X-Naver-Client-Secret": client_key
          }


def search_link(search_term):
    rs = requests.get(url + search_term , headers=header)
    tmp = rs.json()
    #print(tmp['items'])
    total = tmp['total'] #총 검색량
    print("총 검색량: " + str(total))
    if total > 1000: #start가 1000이 넘지 않게 하기 위한 장치
        total = 999
    links = list()  # 링크들 저장할 주소
    st_rcd = rs.status_code
    if st_rcd != 200:  # 검색 결과가 없으면 error
        print("error")
        return -1



    for i in range(0,int(total/100+1)): #0~백단위+1까지
        start = i*100+1 # start는 1000이 최대ㅠ
        rs = requests.get(url + search_term + "&&display=100&&start=" + str(start), headers=header)
        tmp1 = rs.json()
        for j in range(0, 100):
            links.append(tmp1['items'][j]['link'])  # link만 찾아 links에 저

    return links  # 링크가 저장된 배열 리턴

print(len(search_link("룰429")))

print(search_link("룰429"))