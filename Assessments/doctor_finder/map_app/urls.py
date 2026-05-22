from django.urls import path
from . import views

app_name = 'map_app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/doctors/', views.api_doctors_list, name='api_doctors'),
]
