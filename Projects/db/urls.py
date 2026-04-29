from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('showdata/', views.showdata, name='showdata'),
    path('adddata/', views.adddata, name='adddata'),
]