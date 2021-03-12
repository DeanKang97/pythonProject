from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer
from rest_framework import status
from .review_csv import getcomments


# Create your views here.

class ReviewView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            review_queryset = Review.objects.all()  # 모든 Review의 정보를 불러온다.
            review_queryset_serializer = ReviewSerializer(review_queryset, many=True)
            return Response(review_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            review_id = kwargs.get('id')
            review_serializer = ReviewSerializer(Review.objects.get(id=review_id))  # id에 해당하는 Review의 정보를 불러온다
            return Response(review_serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     review_serializer = ReviewSerializer(data=request.data)  # Request의 data를 ReviewSerializer로 변환
    #
    #     if review_serializer.is_valid():
    #         review_serializer.save()  # ReviewSerializer의 유효성 검사를 한 뒤 DB에 저장
    #         return Response(review_serializer.data, status=status.HTTP_201_CREATED)  # client에게 JSON response 전달
    #     else:
    #         return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        answer = getcomments(338641) #가게 코드 받아서 댓글 가져오기
        for i in answer:
            Review.objects.create(menu=i.menu, comment=i.comment,rating=i.rating, time=i.time) #db에 저장
        return Response("answer", status=200)

    # def delete(self, request):
    #     return Response("delete_test_ok", status=200)
