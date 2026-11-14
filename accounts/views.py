from django.contrib.auth import authenticate

#Serializers Import
from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

#permissions Import
from rest_framework.permissions import(
    AllowAny,
)

# Create your views here.
class RegisterUser(CreateAPIView):
    serializer_class=RegisterUserSerializer
    permission_classes=[AllowAny]

class LoginUser(APIView):
    def post(self ,request):
        serializer=LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'Message': "Invalid username or Password"}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Logged in successfully",
            "refresh token": str(refresh),
            "acces token": str(refresh.access_token),
        })

# class ProfileViews(APIView):
