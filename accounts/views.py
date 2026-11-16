from django.contrib.auth import authenticate

#Serializers Import
from .serializers import (
    RegisterSerializer,
    LoginUserSerializer,
    LogoutSerializer
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

#permissions Import
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated
)

#parser
from rest_framework.parsers import(
    MultiPartParser,
    JSONParser,
    FormParser 
)

# Create your views here.
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,JSONParser,FormParser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        return Response({
            "message": "User created Successfully",
            "user Id": user.id,
            "User Name": user.username
        }, status=status.HTTP_200_OK)
    
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

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes = [MultiPartParser,JSONParser,FormParser]

    def post(self, request):
        serializer=LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_205_RESET_CONTENT,
        )