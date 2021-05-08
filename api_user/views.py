from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializers import SummarySerializer
from .models import Summary
from rest_framework import status
from .review_csv import getcomments
from .Language_Processing import countwords


# Create your views here.

class ReviewView(APIView):
    def get(self, request, **kwargs):
        # review_queryset = Review.objects.all()  # 모든 Review의 정보를 불러온다.
        # review_queryset_serializer = ReviewSerializer(review_queryset, many=True)
        # 거짓 판별 리뷰 할떄 사용할 것

        ans = countwords()
        # for i in range(len(ans)):
        #     Summary.objects.create(word=ans[i])
        #
        # summary_set = Summary.objects.all()
        # summary_set_serializer = SummarySerializer(summary_set, many=True)

        return Response(ans, status=status.HTTP_200_OK)

    def put(self, request):

        return Response("hello", status=200)
