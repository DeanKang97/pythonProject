from main import pagingbtn
from main import get_product_name
from main import get_rating
import pandas as pd

get_rating() #total rating csv파일 생성

def makecsv():

    reviews = pagingbtn()
    data = pd.DataFrame(reviews)
    data.columns = ["rating","time","content","label"]
    csv_name = "reviews_"+ get_product_name() +".csv"
    data.to_csv(csv_name, encoding='utf-8-sig')

makecsv()