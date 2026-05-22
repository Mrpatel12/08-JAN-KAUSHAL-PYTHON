from django.urls import path
from . import views

app_name = 'tweets'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/fetch-tweets/', views.fetch_tweets_api, name='fetch_tweets_api'),
    path('api/update-credentials/', views.update_credentials_api, name='update_credentials_api'),
]
