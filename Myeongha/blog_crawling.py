import requests
import time #sleep
from selenium import webdriver #웹드라이버
import csv
from selenium.common.exceptions import  NoSuchElementException #옛날블로그유형을 위한 예외처리



#제품명 지정
product_name = "세라마이드 인텐스 크림"
# print("화장품 검색 :", end='')
# product_name = input()


# 네이버 검색api 주소
url = "https://openapi.naver.com/v1/search/blog?query="

#api 사용자 인증
client_id = "iq6LEjpJhnsJLV5ev7_a"
client_key = "XZIPTU2d03"

header = {"X-Naver-Client-Id": client_id,  # api_key and id
          "X-Naver-Client-Secret": client_key
          }

#검색 결과의 블로그 URL을 리스트로 저장
def search_link(search_term):
    rs = requests.get(url + search_term , headers=header)
    time.sleep(0.1) #에러를 줄이기 위한 sleep
    tmp = rs.json() #json화
    total = tmp['total'] #총 검색량
    #print("첫 총 검색량: " + str(total))
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
        time.sleep(0.1) #에러를 줄이기 위한 sleep
        tmp1 = rs.json()
        for j in range(0, len(tmp1['items'])):
            links.append(tmp1['items'][j]['link'])  # link만 찾아 links에 저장

    return links  # 링크가 저장된 배열 리턴

#블로그링크 리스트 생성
#blog_link = search_link("\""+product_name+"\"") #전체 리뷰
blog_link_truth = search_link("\""+product_name+"\""+" \"내돈내산\"") #진실 리뷰
blog_link_fake = search_link("\""+product_name+"\""+" \"원고료\"") #진실 리뷰

#리뷰 수 가시적을 보기 위한 출력
print("가짜 리뷰 수: "+str(len(blog_link_fake)))
print("진짜 리뷰 수: "+str(len(blog_link_truth)))

#가짜리뷰 저장한 CSV파일 생성
def fake_review(blog_link):
    file_name = "fake_review_" + product_name + ".csv"
    f = open(file_name, 'w', encoding='utf-8-sig', newline='')
    wr = csv.writer(f)
    wr.writerow(["블로그내용"])  # 저장할 csv의 컬럼명 지정

    # 웹드라이버 실행
    options = webdriver.ChromeOptions()  # 크롬 드라이버 옵션
    options.add_argument('headless') #웹드라이버 안키고 사용 옵션
    driver = webdriver.Chrome("C:/Users/Myeongha/Downloads/chromedriver_win32/chromedriver.exe", options=options)

    save_count = 0 #저장된 튜플 수

    # 블로그 글 csv에 저장
    for i in range(0, len(blog_link)):
        # 웹드라이버의 주소 입력

        url = blog_link[i]
        if (url.startswith('https://blog.naver.com') == True):  # 네이버 블로그일 경우에만 내용 크롤링
            driver.get(url)
            time.sleep(3) #나중에 적정시간으로 바꾸도록
            driver.switch_to.frame('mainFrame')
            target_info = {}
            overlays = "div > div > div.se-main-container"
            try:  # 네이버 블로그가 2가지 유형이 있는 듯 (신/옛날)
                # https://blog.naver.com/sobongg/222224328628 가장 자주 보는 신유형
                contents = driver.find_element_by_css_selector(overlays)
                print(contents.text)
                wr.writerow([contents.text])
                save_count += 1

            except NoSuchElementException:
                # https://blog.naver.com/leesin8888/222225179323 뭔가 옛날 유형
                overlays = "#post-view" + url.split('=')[-1]  # 옛날유형 용
                contents = driver.find_element_by_css_selector(overlays)
                print(contents.text)
                wr.writerow([contents.text])
                save_count += 1

            except:
                continue

        if (save_count == 100):  # 리뷰갯수 범위 지정
            break

    f.close


#진짜리뷰 저장한 CSV파일 생성
def truth_review(blog_link):
    file_name = "truth_fake_review_" + product_name + ".csv"
    f = open(file_name, 'w', encoding='utf-8-sig', newline='')
    wr = csv.writer(f)
    wr.writerow(["블로그내용"])  # 저장할 csv의 컬럼명 지정

    # 웹드라이버 실행
    options = webdriver.ChromeOptions()  # 크롬 드라이버 옵션
    options.add_argument('headless') #웹드라이버 안키고 사용 옵션
    driver = webdriver.Chrome("C:/Users/Myeongha/Downloads/chromedriver_win32/chromedriver.exe", options=options)

    save_count = 0#저장된 튜플 수

    # 블로그 글 csv에 저장
    for i in range(0, len(blog_link)):
        # 웹드라이버의 주소 입력

        url = blog_link[i]
        if (url.startswith('https://blog.naver.com') == True):  # 네이버 블로그일 경우에만 내용 크롤링
            driver.get(url)
            time.sleep(3)
            driver.switch_to.frame('mainFrame')
            target_info = {}
            overlays = "div > div > div.se-main-container"
            try:  # 네이버 블로그가 2가지 유형이 있는 듯 (신/옛날)
                # https://blog.naver.com/sobongg/222224328628 가장 자주 보는 신유형
                contents = driver.find_element_by_css_selector(overlays)
                print(contents.text)
                wr.writerow([contents.text])
                save_count += 1

            except NoSuchElementException:
                # https://blog.naver.com/leesin8888/222225179323 뭔가 옛날 유형
                overlays = "#post-view" + url.split('=')[-1]  # 옛날유형 용
                contents = driver.find_element_by_css_selector(overlays)
                print(contents.text)
                wr.writerow([contents.text])
                save_count += 1

            except:
                continue

        if (save_count == 100):  # 리뷰갯수 범위 지정
            break

    f.close


fake_review(blog_link_fake)
truth_review(blog_link_truth)

