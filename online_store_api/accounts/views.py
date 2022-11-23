from django.contrib.auth import get_user_model
from rest_framework import generics as api_generic_views
from rest_framework import permissions, status, authentication
from rest_framework import views as api_views
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import CreateUserSerializer
from django.contrib.auth import logout, login

UserModel = get_user_model()


class RegisterView(api_generic_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(auth_views.ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user=user)
        token = Token.objects.get_or_create(user=user)[0]
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "token": token.key,
                "is_admin": user.is_staff,
            },
        )


class LogoutView(api_views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    @staticmethod
    def __perform_logout(request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            status=status.HTTP_200_OK,
            data={"message": "User Logged out successfully"},
        )

    def get(self, request):
        return self.__perform_logout(request)

    def post(self, request):
        return self.__perform_logout(request)
