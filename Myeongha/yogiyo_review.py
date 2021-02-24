#기본 패키지
import requests
from bs4 import BeautifulSoup
import time
import re
import time
import pickle
import pandas as pd
from tqdm import tqdm
from tqdm import trange
import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver

#from yogiyo_init import restaurant_code

#가게정보DB로 부터 받은 가게코드 값 넣기
restaurant_code = '439809'

headers = {
    'User-Agent': "각자의 User-Agent를 넣어주자",
    'Accept-Language': "ko-KR,ko"
    }


#크롬 웹드라이버 사용
driver = webdriver.Chrome("C:/Users/Myeongha/Downloads/chromedriver_win32/chromedriver.exe")
driver.maximize_window()


#웹드라이버의 주소 입력(요기요)
url = 'https://www.yogiyo.co.kr/mobile/#/'+ restaurant_code
driver.get(url)


#스크롤함수 선언
def scroll():
    prev_height = driver.execute_script("return document.body.scrollHeight")

    # 웹페이지 맨 아래까지 무한 스크롤
    while True:
        # 스크롤을 화면 가장 아래로 내린다
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 페이지 로딩 대기
        time.sleep(2)

        # 현재 문서 높이를 가져와서 저장
        curr_height = driver.execute_script("return document.body.scrollHeight")

        if(curr_height == prev_height):
            break

        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")


#리뷰페이지로 이동하는 함수 선언 및 호출
def go_to_review():
    print('리뷰 페이지 로드중...')
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(2)
    print('리뷰 페이지 로드 완료!')

go_to_review()


#더보기 버튼 누르기
def click_more_review():
    driver.find_element_by_class_name('btn-more').click()
    time.sleep(2)

#리뷰 페이지 모두 펼치기
def stretch_review_page():
    review_count = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)
    click_count = int((review_count/10))
    print('모든 리뷰 불러오기 시작...')
    for _ in trange(click_count):
        try:
            scroll()
            click_more_review()
        except Exception as e:
            pass
    scroll()
    print('모든 리뷰 불러오기 완료!')

stretch_review_page()


#모든 리뷰 가져오는 함수 선언
def get_all_review_elements():
    reviews = driver.find_elements_by_css_selector('#review > li.list-group-item.star-point.ng-scope')
    return reviews


#모든 리뷰를 저장하는 데이터프레임 생성
df = pd.DataFrame(columns=['Restaurant','UserID','Menu','Review',
                                   'Total','Taste','Quantity','Delivery','Date'])
# 해당 음식점의 리뷰 수 만큼 데이터를 가져옴
for review in tqdm(get_all_review_elements()):
                    try:
                        df.loc[len(df)] = {
                            'Restaurant':driver.find_element_by_class_name('restaurant-name').text,
                            'UserID':review.find_element_by_css_selector('span.review-id.ng-binding').text,
                            'Menu':review.find_element_by_css_selector('div.order-items.default.ng-binding').text,
                            'Review':review.find_element_by_css_selector('p').text,
                            'Total':str(len(review.find_elements_by_css_selector('div > span.total > span.full.ng-scope'))),
                            'Taste':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(3)').text,
                            'Quantity':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(6)').text,
                            'Delivery':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(9)').text,
                            'Date':review.find_element_by_css_selector('div:nth-child(1) > span.review-time.ng-binding').text,
                        }
                    except Exception as e:
                        print('리뷰 페이지 에러')
                        print(e)
                        pass


#데이터프레임을 pickle 형태로 저장
def save_pickle(code, yogiyo_df):
    pickle.dump(yogiyo_df, open('./{}_df.pkl'.format(code),'wb'))
    print('{} pickle save complete!'.format(code))

save_pickle(restaurant_code, df)

#데이터프레임 오픈
with open('./{}_df.pkl'.format(restaurant_code), 'rb') as f:
    data = pickle.load(f)

data  #주피터확인용



