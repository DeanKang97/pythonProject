from main import pagingbtn
import csv


def makecsv():
    reviews = pagingbtn()
    review_num = 0 #리뷰 넘버
    f = open('reviews.csv', 'w', encoding='utf-8-sig', newline='')
    wr = csv.writer(f)
    wr.writerow(["No.","평점","작성시간","리뷰내용"]) #저장할 csv의 컬럼명
    for review in reviews:
        #리뷰 넘버 증가
        review_num+=1
        #CSV에 리뷰넘버, 평점, 작성시간, 리뷰내용 삽입
        wr.writerow([review_num,review.rating.replace("평점",""), review.writing_time, review.review_content.replace("\n"," ")])

    f.close()

makecsv()
