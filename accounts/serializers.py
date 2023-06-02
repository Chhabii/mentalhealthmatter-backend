from rest_framework import serializers
from .models import User 
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email','password']

    def create(self,validated_data):
        user = super(UserSerializer,self).create(validated_data)
        user.password = make_password(validated_data['password'])
        user.save()
        return user


    
    
