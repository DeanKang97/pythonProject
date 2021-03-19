from main import pagingbtn
import csv


def makecsv():
    reviews = pagingbtn()
    f = open('reviews.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for review in reviews:
        wr.writerow([review.rating, review.writing_time, review.review_title, review.review_content])

    f.close()

makecsv()