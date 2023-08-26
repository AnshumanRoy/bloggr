from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer, BioUpdateSerializer, ProfilePictureUpdateSerializer, UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
import os
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        custom_response = {
            'refresh': refresh_token,
            'access': access_token,
        }
        return Response(custom_response)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        custom_response = {
            'access': access_token,
        }
        return Response(custom_response)

class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BioUpdateView(APIView):
    def put(self, request):
        user = request.user
        serializer = BioUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfilePictureUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        user = request.user
        
        if user.profile_picture:
            image_path = user.profile_picture.path
            if os.path.exists(image_path):
                os.remove(image_path)
        
        serializer = ProfilePictureUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProfilePictureView(APIView):
    def post(self, request):
        user = request.user
        if user.profile_picture == 'default_pfp.png':
            return Response({'message': 'No profile picture found.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.profile_picture.delete()
            user.profile_picture = 'default_pfp.png'  
            user.save()
            return Response({'message': 'Profile picture deleted and set to default.'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            # return Response(token)
            token.blacklist()

            return Response({"message": "Logged Out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUserProfile(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Object not found."}, status=status.HTTP_404_NOT_FOUND)

class MyProfile(APIView):
    def get(self, request):
        user = request.user
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Object not found."}, status=status.HTTP_404_NOT_FOUND)