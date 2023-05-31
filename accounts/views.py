from .serializers import UserSerializer
from .models import User 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def api_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email,password)
    
    try:
        user = User.objects.get(email=email)
        if not check_password(password,user.password):
            print("password did not match")
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({'error':'Invalid Login Credentials'},status=status.HTTP_400_BAD_REQUEST)
    request.session['user_id'] = user.id 
    print(request.session['user_id'])
    return Response(UserSerializer(user).data)


from django.contrib.auth import logout
@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({"message":"Logged out successfully."},status=200)
