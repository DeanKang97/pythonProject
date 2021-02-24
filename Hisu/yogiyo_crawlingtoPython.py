import pickle
# 기본 패키지
import time
import warnings

import pandas as pd
from tqdm import tqdm
from tqdm import trange
from selenium import webdriver

warnings.filterwarnings('ignore')

# 크롤링 패키지

headers = {
    "User-Agent": "각자의 User-Agent를 넣어주자",
    "Accept-Language": "ko-KR,ko"
}
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")

driver = webdriver.Chrome('Your driver Path... 시바 안해먹음 ')
driver.maximize_window()

url = 'https://www.yogiyo.co.kr'
driver.get(url)


def set_location(location):
    print(location + '으로 위치 설정 하는중...')
    driver.find_element_by_css_selector('.input-group > form > input').click()
    driver.find_element_by_css_selector('#button_search_address > button.btn-search-location-cancel.btn-search-location.btn.btn-default > span').click()
    driver.find_element_by_name('address_input').send_keys(location)
    driver.find_element_by_xpath('//*[@id="search"]/div/form/input')



    # driver.find_element_by_css_selector('#search> div > form > input')
    driver.find_element_by_css_selector('#button_search_address > button.btn.btn-default.ico-pick').click()
    time.sleep(2)
    print(location + '으로 위치 설정 완료!')


# search > div > form > input
set_location('가톨릭대 성심교정')

food_dict = {'프랜차이즈': 3, '치킨': 4, '피자&양식': 5, '중국집': 6,
             '한식': 7, '일식&돈까스': 8, '족발&보쌈': 9, '야식': 10,
             '분식': 11, '카페&디저트': 12}


# 요기요 카테고리 Element Number Dictionary 정의

def go_to_category(category):
    print(category + '카테고리 페이지 로드중')
    driver.find_element_by_xpath('//*[@id="category"]/ul/li[{}]/span'.format(food_dict.get(category))).click()
    time.sleep(3)
    print(category + '카테고리 페이지 로드 완료')


go_to_category('치킨')


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

        if (curr_height == prev_height):
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")



def search_restaurant(restaurant_name):
    try:
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        print('1')
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(restaurant_name)
        print('1')
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
    except Exception as e:
        print('search_restaurant 에러')
    time.sleep(5)


search_restaurant('동대문엽기떡볶이-역곡점')


def go_to_restaurant():
    try:
        driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div').click()
    except Exception as e:
        print('go_to_restaurant 에러')
    time.sleep(5)


go_to_restaurant()


def go_to_review():
    print('리뷰 페이지 로드중...')
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(2)
    print('리뷰 페이지 로드 완료!')


go_to_review()


def click_more_review():
    driver.find_element_by_class_name('btn-more').click()
    time.sleep(2)


def stretch_review_page():
    review_count = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)
    click_count = int((review_count / 10))
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


def get_all_review_elements():
    reviews = driver.find_elements_by_css_selector('#review > li.list-group-item.star-point.ng-scope')
    return reviews


df = pd.DataFrame(columns=['Restaurant', 'UserID', 'Menu', 'Review',
                           'Total', 'Taste', 'Quantity', 'Delivery', 'Date'])

for review in tqdm(get_all_review_elements()):  # 해당 음식점의 리뷰 수 만큼 데이터를 가져옴
    try:
        df.loc[len(df)] = {
            'Restaurant': driver.find_element_by_class_name('restaurant-name').text,
            'UserID': review.find_element_by_css_selector('span.review-id.ng-binding').text,
            'Menu': review.find_element_by_css_selector('div.order-items.default.ng-binding').text,
            'Review': review.find_element_by_css_selector('p').text,
            'Total': str(len(review.find_elements_by_css_selector('div > span.total > span.full.ng-scope'))),
            'Taste': review.find_element_by_css_selector(
                'div:nth-child(2) > div > span.category > span:nth-child(3)').text,
            'Quantity': review.find_element_by_css_selector(
                'div:nth-child(2) > div > span.category > span:nth-child(6)').text,
            'Delivery': review.find_element_by_css_selector(
                'div:nth-child(2) > div > span.category > span:nth-child(9)').text,
            'Date': review.find_element_by_css_selector('div:nth-child(1) > span.review-time.ng-binding').text,
        }
    except Exception as e:
        print('리뷰 페이지 에러')
        print(e)
        pass


def save_pickle(location, category, yogiyo_df):
    pickle.dump(yogiyo_df, open('./{}_{}_df.pkl'.format(location, category), 'wb'))
    print('{} {} pikcle save complete!'.format(location, category))


save_pickle('./data/가톨릭대 성심교정2', '치킨', df)

with open('./data/가톨릭대 성심교정2_치킨_df.pkl', 'rb') as f:
    data = pickle.load(f)

driver.quit()
