from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # send verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        site = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        verify_url = f"{site}/api/v1/accounts/auth/verify-email/?uid={uid}&token={token}"
        subject = 'Verify your email for FarmLedger'
        message = f'Welcome {user.email}! Verify your email by visiting: {verify_url}'
        send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@farmledger.local'), [user.email], fail_silently=True)


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        if not uid or not token:
            return Response({'detail': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except Exception:
            return Response({'detail': 'Invalid uid'}, status=status.HTTP_400_BAD_REQUEST)
        if default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({'detail': 'Email verified'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        site = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        reset_url = f"{site}/api/v1/accounts/auth/password-reset-confirm/?uid={uid}&token={token}"
        subject = 'Reset your FarmLedger password'
        message = f'Hi {user.email}, reset your password by visiting: {reset_url}'
        send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@farmledger.local'), [user.email], fail_silently=True)
        return Response({'detail': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        if not uid or not token or not new_password:
            return Response({'detail': 'uid, token and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except Exception:
            return Response({'detail': 'Invalid uid'}, status=status.HTTP_400_BAD_REQUEST)
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password has been reset'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)
