from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root),
    path('getall/', views.getall),
    path('getsingle/<int:id>/', views.getsingle),
    path('postdata/', views.postdata),
    path('updatedata/<int:id>/', views.updatedata),
    path('deletedata/<int:id>/', views.deletedata),
]
