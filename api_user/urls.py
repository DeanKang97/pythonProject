from django.urls import path
from . import views

app_name = 'api_user'
urlpatterns = [
    path('', views.ReviewView.as_view()),
    path('<int:user_id>', views.ReviewView.as_view())
]
