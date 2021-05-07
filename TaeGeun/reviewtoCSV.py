from main import pagingbtn
import csv
import pandas as pd



def makecsv():
    reviews = pagingbtn()
    data = pd.DataFrame(reviews)
    data.columns = ["rating","time","content","label"]
    data.to_csv('reviews.csv',encoding='utf-8')
    # f = open('reviews.csv', 'w', encoding='utf-8', newline='')
    # wr = csv.writer(f)
    # for review in reviews:
    #     wr.writerow([review.rating, review.writing_time, review.review_title, review.review_content, review.label])
    #
    # f.close()

makecsv()