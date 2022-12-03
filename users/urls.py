from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework import routers
from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    ClientViewSet,
    UserViewSet,
    SupportViewSet,
    AdminViewSet,
    DirectionViewSet,
    MapViewSet,
    ResetPasswordByPhoneAPIView,
    ResetPasswordAPIView,
    ForgotPasswordByPhoneAPIView,
    ForgotPasswordAPIView,
    UserContactViewSet,
    ApproveUserViewSet,
    FacebookLogin,
    GoogleLogin,
    ResetPasswordView,
    RegisterPhone,
    UserProfileViewSet,
    CurrentUserView,
    ChangePasswordView,
    ArchiveUserViewSet,
    ArchiveListUserViewSet,
    GetTariffViewSet,
    TariffViewSet,
    PropsViewSet,
)


users_router = routers.DefaultRouter()
users_router.register(r'clients', ClientViewSet, basename='clients')
users_router.register(r'supports', SupportViewSet, basename='supports')
users_router.register(r'admins', AdminViewSet, basename='admins')
users_router.register(r'all-users', UserViewSet, basename='all-users')
users_router.register(r'followers', UserContactViewSet, basename='followers')
users_router.register(r'approve-user', ApproveUserViewSet, basename='approve-user')
users_router.register(r'address', DirectionViewSet,  basename='address')
users_router.register(r'map', MapViewSet,  basename='map')
users_router.register(r'users-profile', UserProfileViewSet, basename='users-profile')
users_router.register(r'archive-user', ArchiveUserViewSet, basename='archive-users')
users_router.register(r'archive-list', ArchiveListUserViewSet, basename='archive-list')
users_router.register(r'create-tariff', TariffViewSet, basename='create-tariff')
users_router.register(r'get-tariff', GetTariffViewSet, basename='get-tariff')
users_router.register(r'props', PropsViewSet, basename='props')


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("register-phone/", RegisterPhone.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("obtain/", TokenObtainPairView.as_view()),
    path("api/register/email_verify/", VerifyEmailView.as_view(), name="email_verify"),
    path('forgot/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('forgot-phone/', ForgotPasswordByPhoneAPIView.as_view(), name='forgot-password-by-phone'),
    path('reset-phone/', ResetPasswordByPhoneAPIView.as_view(), name='reset-password-by-phone'),
    path('facebook', FacebookLogin.as_view(), name='facebook'),
    path('google', GoogleLogin.as_view(),  name='google'),
    path('me', CurrentUserView.as_view(),  name='me'),
    path("reset-password/<int:pk>", ResetPasswordView.as_view(), name="change-password"),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
