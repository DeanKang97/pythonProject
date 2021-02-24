import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


headers = {
    'User-Agent': "각자의 User-Agent를 넣어주자",
    'Accept-Language': "ko-KR,ko"
    }

#추후에 가게정보DB에서 가게명 받아오면 됨
restaurant_name = 'BHC치킨 여수엑스포광장점 '

#크롬 웹드라이버 사용
driver = webdriver.Chrome("C:/Users/Myeongha/Downloads/chromedriver_win32/chromedriver.exe")
driver.maximize_window()


#웹드라이버의 주소 입력(카카오맵)
url = 'https://map.kakao.com/'
driver.get(url)
time.sleep(2)

#검색창에 가게이름 검색
def input_restaurant_name(input) :
    #driver.find_element_by_xpath('//*[@id="search.keyword"]/fieldset/div[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="search.keyword.query"]').send_keys(input)
    print("가게명 입력")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="search.keyword.query"]').send_keys(Keys.ENTER)

input_restaurant_name(restaurant_name)
time.sleep(2)

#가게 주소 가져오기
address = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div[7]/div[5]/ul/li[1]/div[5]/div[2]/p[1]').get_attribute('title')
print("주소: "+address)

#웹드라이버 요기요로 이동
driver.get("https://www.yogiyo.co.kr")
time.sleep(1)

#위치 설정 함수 선언 및 사용
def set_location(location):
    print('\''+location+'\'으로 위치 설정 하는중...')
    driver.find_element_by_css_selector('#search > div > form > input').click()
    driver.find_element_by_css_selector('#button_search_address > button.btn-search-location-cancel.btn-search-location.btn.btn-default > span').click()
    driver.find_element_by_css_selector('#search > div > form > input').send_keys(location)
    driver.find_element_by_css_selector('#button_search_address > button.btn.btn-default.ico-pick').click()
    time.sleep(2)
    if (driver.current_url == 'https://www.yogiyo.co.kr/mobile/#/') :
        print("가게 위치가 아닌 인근 위치로 주소 변경")
        driver.find_element_by_xpath('//*[@id="search"]/div/form/ul/li[3]/a').click()
        location = '가게 인근 위치명'
        time.sleep(2)
    print('\''+location+'\'으로 위치 설정 완료!')


#가게위치를 바탕으로 가게 검색
set_location(address)


#가게 찾는 함수 선언 및 호출
def search_restaurant(restaurant_name):
    try:
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        #print('1')
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(restaurant_name)
        #print('1')
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
    except Exception as e:
        print('search_restaurant 에러')
    time.sleep(2)

search_restaurant(restaurant_name)


#해당 가게 페이지 들어가는 함수 선언 및 호출
def go_to_restaurant():
    try:
        driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div').click()
    except Exception as e:
        print('go_to_restaurant 에러')
    time.sleep(2)

go_to_restaurant()


#현재 URL 가져오고 요기요 가게 코드 가져오기
url_now = driver.current_url
restaurant_code = url_now.replace("https://www.yogiyo.co.kr/mobile/#/", "")
restaurant_code = restaurant_code[:restaurant_code.index("/")]
print("해당 가게의 요기요 넘버: "+ restaurant_code)

# 가게 코드를 추후 가게정보DB에 저장하면 됨
