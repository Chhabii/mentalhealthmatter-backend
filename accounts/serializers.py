from rest_framework import serializers
from .models import User 
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email','password']
    
    
