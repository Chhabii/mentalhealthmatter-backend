from .serializers import UserSerializer
from .models import User 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token

from apis.models import StressLevel,Conversation

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({**serializer.data,'token':token.key},status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email,password)
    
    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            print("password did not match")
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({'error':'Invalid Login Credentials'},status=status.HTTP_400_BAD_REQUEST)
    # request.session['user_id'] = user.id 
    # print(request.session['user_id'])
    token,created = Token.objects.get_or_create(user=user)
    return Response({'user':UserSerializer(user).data,'token':token.key},status=status.HTTP_200_OK)


from django.contrib.auth import logout
@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({"message":"Logged out successfully."},status=200)
