import requests

url = "https://openapi.naver.com/v1/search/blog?query="  # 네이버 검색 api

client_id = "iq6LEjpJhnsJLV5ev7_a"
client_key = "XZIPTU2d03"

header = {"X-Naver-Client-Id": client_id,  # api_key and id
          "X-Naver-Client-Secret": client_key
          }


def search_link(search_term):
    rs = requests.get(url + search_term + "&&display=100&&start=1", headers=header)
    tmp = rs.json()
    links = list()  # 링크들 저장할 주소
    start = 1
    st_rcd = rs.status_code
    if st_rcd != 200:  # 검색 결과가 없으면 error
        print("error")
        return -1

    total = tmp['total']  # 검색 결과 수를 받아와서 그만큼 반복

    for i in range(total):
        rs = requests.get(url + search_term + "&&display=100&&start=" + str(start), headers=header)

        tmp = rs.json()

        for i in range(0, len(tmp['items'])):
            links.append(tmp['items'][i]['link'])  # link만 찾아 links에 저
        start += 1

    return links  # 링크가 저장된 배열 리턴



