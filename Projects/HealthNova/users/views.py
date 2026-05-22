from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import RegisterForm, LoginForm

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LandingView(TemplateView):
    template_name = 'users/landing.html'


class RegisterPageView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        data = form.cleaned_data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super().form_valid(form)


class LoginPageView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('landing')

    def form_valid(self, form):
        data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
        serializer = CustomTokenObtainPairSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # show tokens on a simple page
        return render(self.request, 'users/login_success.html', {'token_data': serializer.validated_data})
