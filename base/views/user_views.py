from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import serializers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from base.models import Product
from base.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user): This is for adding info to token which can be retrieved after decoding
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'hello world'

    #     return token
    
    # This is for customizing json response of CBV api view
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        
        for k, v in serializer.items():
            data[k] = v
        # data['username'] = self.user.username
        # data['email'] = self.user.email      
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
  
  
@api_view(['POST'])  
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name= data['name'],
            username = data['email'],
            email = data['email'],
            password  = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        
        return Response(serializer.data)
    except:
        message = {'detail' : 'User with this email already exist'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user= request.user
    # after updating we want new token for the user,thats why used UserSerailizerwithtoken
    serializer = UserSerializerWithToken(user,many=False)
    
    data= request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    
    if data['password'] != '' :
        user.password = make_password(data['password'])
    
    user.save()
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user= request.user
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

# for admin purpose
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
    user= User.objects.get(id=pk)
    
    data= request.data
    
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    
    user.save()
    
    serializer = UserSerializer(user,many=False)
    
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request,pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')
    
