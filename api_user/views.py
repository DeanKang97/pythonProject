from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Language_Processing import countwords
import csv
# Create your views here.


class ReviewView(APIView):
    def get(self, request, **kwargs):
        rq = request.GET.get('key')
        review = request.GET.get('review')
        if not review:
            ans = countwords(rq)
            return Response(ans, status=status.HTTP_200_OK)
        else:
            csv_file= open("/Users/deankang/Documents/Github/pythonProject/api_user/reviews_" + rq + ".csv", 'r')
            c = csv.DictReader(csv_file)
            data_list = []

            for rows in c:

                data = {}
                data['id'] = rows['\ufeff']
                data['content'] = rows['content']
                data['truth'] = rows['ans']
                data_list.append(data)

            return Response(data_list, status=status.HTTP_200_OK)

    def put(self, request):

        return Response('hi', status=200)
