from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    ClientViewSet,
    UserViewSet,
    SupportViewSet,
    AdminViewSet,
    AddressViewSet,
    MapViewSet,
    ResetPasswordByPhoneAPIView,
    ResetPasswordAPIView,
    ForgotPasswordByPhoneAPIView,
    ForgotPasswordAPIView,
    CustomUserCreate,
)


users_router = DefaultRouter()

users_router.register(r'clients', ClientViewSet, basename='clients')
users_router.register(r'supports', SupportViewSet, basename='supports')
users_router.register(r'admins', AdminViewSet, basename='admins')
users_router.register(r'all-users', UserViewSet, basename='all-users')
users_router.register(r'address', AddressViewSet)
users_router.register(r'map', MapViewSet)


urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("obtain/", TokenObtainPairView.as_view()),
    path("api/register/email_verify/", VerifyEmailView.as_view(), name="email_verify"),
    path('forgot/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('forgot-phone/', ForgotPasswordByPhoneAPIView.as_view(), name='forgot-password-by-phone'),
    path('reset-phone/', ResetPasswordByPhoneAPIView.as_view(), name='reset-password-by-phone'),
]
