from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
import json
from django.contrib.auth.hashers import make_password, check_password

# hashed_pwd = make_password("plain_text")
# check_password("plain_text",hashed_pwd)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(request.data.get('password'), user.password):
            return Response({"password": "Password doesn't match"}, status=status.HTTP_400_BAD_REQUEST)

        data = {**request.data, 'username': user.username}
        serializer = self.serializer_class(data=data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user.organization,
        })
    

class CustomRegisterToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        data =  {**request.data,  'password':  make_password(request.data.get('password'))}
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user.organization,
        }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GetWorkspace(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WorkspaceForm.objects.all()
    serializer_class =  WorkspaceFormSerializer

    def get_queryset(self):
        user = self.request.user
        return WorkspaceForm.objects.filter(user=user)


class GetWorkspaceById(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = WorkspaceForm.objects.all()
    serializer_class =  WorkspaceFormSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     return WorkspaceForm.objects.filter(user=user)


class AddWorkspace(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WorkspaceForm.objects.all()
    serializer_class =  AddWorkspaceFormSerializer

    def create(self, request, *args, **kwargs):
        pythonObj =  json.loads(request.data['data'])
        pythonObj['description']['image'] = request.FILES['image']
        serializer = self.get_serializer(data=pythonObj)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        

class GetLocations(generics.ListAPIView):
    queryset =  Location.objects.all()

    def list(self, request, *args,  **kwargs):
        country = Location.objects.values_list('country', 'city','area')

        data =  {'locations': country}
        return Response(data)
    

class SearchByLocation(generics.ListAPIView):
    
    queryset =  WorkspaceForm.objects.all()
    serializer_class = WorkspaceFormSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.GET.get('country')
        city = self.request.GET.get('city')
        area = self.request.GET.get('area')
        
        if country:
            queryset = queryset.filter(location__country__icontains=country)
        if city:
            queryset = queryset.filter(location__city__icontains=city)
        if area:
            queryset = queryset.filter(location__area__icontains=area)
        
        return queryset


class GetKeys(generics.ListAPIView):
    
    queryset =  WorkspaceForm.objects.all()
    serializer_class = WorkspaceFormSerializer

    def get(self, request, *args, **kwargs):
        print(settings.AWS_STORAGE_BUCKET_NAME,
settings.AWS_S3_ACCESS_KEY_ID,
settings.AWS_S3_SECRET_ACCESS_KEY,
settings.AWS_S3_REGION_NAME,
settings.AWS_DEFAULT_ACL,
settings.AWS_S3_ENDPOINT_URL)
        return self.list(request, *args, **kwargs)