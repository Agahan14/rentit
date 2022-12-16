import jwt
import random
import string
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import (
    generics,
    status,
    viewsets,
    exceptions,
    filters,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAcceptable,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from rentit import settings
from .models import (
    User,
    Direction,
    Map,
    PasswordReset,
    PasswordResetByPhone,
    FollowingSystem,
    Tariff,
    GetTariff,
    Props,
)
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
    UserListSerializer,
    UserMiniSerializer,
    DirectionSerializer,
    MapSerializer,
    UserContactSerializer,
    UserFollowingSerializer,
    ApproveUserSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ArchiveUserSerializer,
    PropsSerializer,
    GetTariffSerializer,
    TariffSerializer,
    FavoriteProductsSerializer,
)
from .utils import Util


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data

            user = User.objects.get(email=user_data["email"])
            token = RefreshToken.for_user(user)
            current_site = request.get_host()
            link = reverse("email_verify")
            url = "http://" + current_site + link + "?token=" + str(token)
            body = "Hi " + " Use the link below to verify your email \n" + url
            data = {
                "email_body": body,
                "to_email": user.email,
                "email_subject": "Verify your email",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]


    def get(self, request):
        token = request.GET.get("token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        user = User.objects.get(id=payload["user_id"])
        try:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return render(request, 'index.html')
                # return Response(
                #     {"email": "Successfully activated"}, status=status.HTTP_200_OK
                # )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'first_name': user.first_name,
                'email': user.email,
                'user_type': user.user_type,
                'user_pictures': str(user.pictures),
                'followers': str(user.followers.count()),
                'followings': str(user.following.count()),
                'user_id': str(user.id),
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ForgotPasswordByPhoneAPIView(APIView):
    def post(self, request):
        phone = request.data['phone']
        print(request.data['phone'])
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise NotAcceptable("Please enter a valid phone.")
        token = ''.join(random.choice(string.digits) for _ in range(4))

        PasswordResetByPhone.objects.create(phone=phone, token=token)

        account_sid = "ACbaed99a5ff0ae25a71bc4698ac44bebd"
        auth_token = "121d2d48369669f150c70792c7c44773"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Your verification PIN is: ' + token,
            from_="+18317447330",
            to=phone,
        )

        return Response({
            'message': 'Please check your phone!'
        })


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotAcceptable("Please enter a valid email.")
        token = ''.join(random.choice(string.digits) for _ in range(4))

        PasswordReset.objects.create(email=email, token=token)

        send_mail(
            subject='Reset your password!',
            message='Use this code to reset your password: ' + token,
            from_email=getattr(settings, 'EMAIL_HOST_USER'),
            recipient_list=[email]
        )

        return Response({
            'message': 'Please check your email!'
        })


class ResetPasswordAPIView(APIView):
    def post(self, request):
        data = request.data

        passwordReset = PasswordReset.objects.filter(token=data['token']).first()

        if data['token'] != passwordReset.token:
            raise exceptions.APIException('Code is incorrect!')

        user = User.objects.filter(email=passwordReset.email).first()

        if not user:
            raise exceptions.NotFound('User not found!')

        user_id = user.pk
        return Response({
            'message': 'success',
            'user': str(user_id)
        })


class ResetPasswordByPhoneAPIView(APIView):
    def post(self, request):
        data = request.data

        passwordResetByPhone = PasswordResetByPhone.objects.filter(token=data['token']).first()

        if data['token'] != int(passwordResetByPhone.token):
            raise exceptions.APIException('Code is incorrect!')

        user = User.objects.filter(phone=passwordResetByPhone.phone).first()

        if not user:
            raise exceptions.NotFound('User not found!')

        user_id = user.pk
        return Response({
            'message': 'success',
            'user': user_id
        })


class ResetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='client').filter(is_archive=False)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    # permission_classes = (IsSuperUser,)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_archive=False)
    serializer_class = UserProfileSerializer
    
    # def get_queryset(self):
    #     return User.objects.filter(id=self.request.user.id)
    # http_method_names = ['get', 'put', 'patch']
    # permission_classes = (IsSuperUser,)


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_archive=False)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ('birth_date', 'first_name', 'email', 'phone')
    search_fields = ['email', 'phone', 'first_name', 'last_name', ]


class SupportViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='support').filter(is_archive=False)
    serializer_class = UserMiniSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='admin')
    serializer_class = UserMiniSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class UserContactViewSet(viewsets.ViewSet):
    serializer_class = UserContactSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def create(self, request):
        serializer = UserContactSerializer(data=request.data)
        if serializer.is_valid():
            # user being followed
            to_user = User.objects.get(id=serializer.data['user_to'])

            # you cant follow yourself lol
            if self.request.user != to_user:
                try:
                    if serializer.data['action'] == 'follow':
                        FollowingSystem.objects.get_or_create(user_from=self.request.user, user_to=to_user)

                    if serializer.data['action'] == 'unfollow':
                        FollowingSystem.objects.filter(user_from=self.request.user, user_to=to_user).delete()

                    followers_followings = UserFollowingSerializer(self.request.user)
                    return Response(followers_followings.data)

                except:
                    return Response({'status': 'error'})
            else:
                return Response({'status': 'no need to follow yourself'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # authenticated user can search for any user's public info
    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserFollowingSerializer(user)
        return Response(serializer.data)


class ApproveUserViewSet(viewsets.ModelViewSet):
    serializer_class = ApproveUserSerializer
    queryset = User.objects.filter(is_active=False)
    lookup_field = 'id'


class ArchiveUserViewSet(viewsets.ModelViewSet):
    serializer_class = ArchiveUserSerializer
    queryset = User.objects.filter(is_archive=False)
    lookup_field = 'id'


class ArchiveListUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserMiniSerializer
    queryset = User.objects.filter(is_archive=True)
    lookup_field = 'id'


class TariffViewSet(viewsets.ModelViewSet):
    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()


class GetTariffViewSet(viewsets.ModelViewSet):
    serializer_class = GetTariffSerializer
    queryset = GetTariff.objects.all()


class PropsViewSet(viewsets.ModelViewSet):
    serializer_class = PropsSerializer
    queryset = Props.objects.all()


def index(request):
    return render(request, 'index.html')


class FavoriteProductViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteProductsSerializer
    queryset = User.objects.all()