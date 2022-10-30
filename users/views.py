import jwt, random, string
from django.urls import reverse
from django.core.mail import send_mail
from rentit import settings
from rest_framework import (
    generics,
    status,
    viewsets,
    exceptions,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAcceptable,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from .utils import Util
from .models import (
    User,
    Address,
    Map,
    PasswordReset,
    PasswordResetByPhone,
)
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
    UserListSerializer,
    AddressSerializer,
    MapSerializer,
    CustomUserSerializer,
)
from .permissions import (
    IsClient,
    IsSuperUser,
)


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                return Response(
                    {"email": "Successfully activated"}, status=status.HTTP_200_OK
                )
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
                "status": "You successfully logged in",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ForgotPasswordByPhoneAPIView(APIView):
    def post(self, request):
        phone = request.data['phone']
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise NotAcceptable("Please enter a valid phone.")
        token = ''.join(random.choice(string.digits) for _ in range(6))

        PasswordResetByPhone.objects.create(phone=phone, token=token)

        account_sid = "ACdeb64be8247471d24bf58c28e45b89ac"
        auth_token = "a857b4819bc02678ef1693c63bf9307b"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Your verification PIN is: ' + token,
            from_="+16802195991",
            to=request.data['phone'],
        )

        print(message.sid)

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
        token = ''.join(random.choice(string.digits) for _ in range(6))

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

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match')

        passwordReset = PasswordReset.objects.filter(token=data['token']).first()

        user = User.objects.filter(email=passwordReset.email).first()

        if not user:
            raise exceptions.NotFound('User not found!')

        # PasswordReset.objects.update(token="agahasndasd")

        user.set_password(data['password'])
        # passwordReset.save()

        user.save()

        return Response({
                'message': 'success'
            })


class ResetPasswordByPhoneAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match')

        passwordResetByPhone = PasswordResetByPhone.objects.filter(token=data['token']).first()

        user = User.objects.filter(phone=passwordResetByPhone.phone).first()

        if not user:
            raise exceptions.NotFound('User not found!')


        user.set_password(data['password'])

        user.save()

        return Response({
                'message': 'success'
            })


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    # permission_classes = (IsSuperUser,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class SupportViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True).filter(is_superuser=False)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
