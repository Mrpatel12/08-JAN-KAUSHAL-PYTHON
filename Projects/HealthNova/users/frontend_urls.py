from django.urls import path
from .views import LandingView, RegisterPageView, LoginPageView

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('signup/', RegisterPageView.as_view(), name='signup'),
    path('signin/', LoginPageView.as_view(), name='signin'),
]
