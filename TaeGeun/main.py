import time
import warnings

warnings.filterwarnings('ignore')
from selenium import webdriver

options = webdriver.ChromeOptions()  # 크롬 드라이버 옵션
options.add_argument('headless')
options.add_argument('lang=ko_KR')  # 웹 브라우저 안키고 실행 & 한국어 인코딩 설정
driver = webdriver.Chrome("../../../../PycharmProjects/pythonProject/chromedriver.exe", options=options)

url = 'https://search.shopping.naver.com/catalog/24365537530'
#https://search.shopping.naver.com/catalog/13642088554 닥터지 레드 블레미쉬 수딩 토너
# https://search.shopping.naver.com/catalog/21754707946?cat_id=50000440&frm=NVSCPRO&query=%EB%A7%88%EB%AA%BD%EB%93%9C+%EC%84%B8%EB%9D%BC%EB%A7%88%EC%9D%B4%EB%93%9C+%EC%9D%B8%ED%85%90%EC%8A%A4+%ED%81%AC%EB%A6%BC&NaPm=ct%3Dkn6zixw8%7Cci%3D0094ebf6b79875e71fad391b8887525103526bec%7Ctr%3Dsls%7Csn%3D95694%7Chk%3D1b47e55449cbb34045bc121d00a50b850516662d
#마몽드 세라마이드 인텐스 크림
driver.get(url)  # url 설정

class Reivews:
    rating = ""
    writing_time = ""
    review_title = ""
    review_content = ""
    label = 0
    def __init__(self, rating, writing_time, review_title, review_content, label) -> object:
        self.rating = rating
        self.writing_time = writing_time
        self.review_title = review_title
        self.review_content = review_content
        self.label = label


def clickmenu():  # 쇼핑몰 리뷰 버튼 누르기 & 화장품은 li:nth-child(5) 해야함
    driver.find_element_by_css_selector('#snb > ul > li:nth-child(5)').click()


def makepgnum(pages):  # 페이징 버튼 가져온 후 리스트로 변환 & '현재페이지' 텍스트 제거
    res = list()
    t = "현재 페이지\n"
    for i in pages:
        res.append(i.text.replace(t, '').strip())

    return res


def crolreview(review, ans):  # 리뷰 객체 가져와서 평점, 시간, 리뷰 제목, 리뷰 내용 출략

    for comment in review:
        rating = comment.find_element_by_css_selector('div >span')
        review_time = comment.find_element_by_css_selector('div > span:nth-child(4)')

        print(rating.text +" "+ review_time.text)
        review_title = comment.find_element_by_css_selector('div.reviewItems_review__1eF8A > div>em')
        review_content = comment.find_element_by_css_selector('div.reviewItems_review__1eF8A > div>p')

        # if rating.text > "3":
        #     ans.append(Reivews(rating.text, review_time.text, review_title.text, review_content.text, 1))
        # else:
        #     ans.append(Reivews(rating.text, review_time.text, review_title.text, review_content.text, 0))

        if rating.text == "평점4" or rating.text == "평점5":
            ans.append([rating.text, review_time.text, review_content.text, 1])
        else:
            ans.append([rating.text, review_time.text, review_content.text, 0])
        print("제목:" + review_title.text + "\n " + review_content.text + "\n\n\n")

    return ans



def pagingbtn():  # 페이지 이동 및 리뷰 가져오는 메인 모듈
    clickmenu()  # 쇼핑몰 리뷰 버튼
    i = 0
    res = list()
    page_bar = driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4')
    pages = page_bar.find_elements_by_tag_name('a')  # 페이지 수 및 현재 페이지
    nu = makepgnum(pages)

    while True:
        if nu[i] in ["맨앞", "이전", "맨뒤"]:  # 맨앞, 이전, 맨뒤 이면 click하지 않고 넘김
            i += 1
            continue

        time.sleep(0.5)
        review_list = driver.find_element_by_css_selector('#section_review > ul')
        review = review_list.find_elements_by_css_selector('li')  # 리뷰 객체 가져옴

        res = crolreview(review,res)  # 리뷰 객체 반환

        current_page = page_bar.find_element_by_css_selector('a.pagination_now__gZWGP')
        current_index = str(current_page.text)[7:]  # 현재 페이지 반환
        print("페이지:" + current_index)  # 현재 페이지 출력
        try:
            if int(nu[i]) % 10 == 0:  # 페이지 수가 10의 배수 즉 마지막 페이지 일때 '다음'버튼을 누르고 새로운 페이지 수 객체를 받음
                i += 1

                pages[i].click()
                time.sleep(1)
                page_bar = driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4')
                pages = page_bar.find_elements_by_tag_name('a')
                nu = makepgnum(pages)
                i = 0
            else:  # 다음 페이지 클릭
                i += 1
                pages[i].click()

        except:
            return res



