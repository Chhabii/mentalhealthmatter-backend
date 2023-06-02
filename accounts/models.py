# from django.db import models
# from django.contrib.auth.hashers import make_password

# class User(models.Model):
#     email = models.EmailField(unique=True,null=False,blank=False)
#     password = models.CharField(max_length=255,null=False,blank=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def save(self,*args,**kwargs):
#         self.password = make_password(self.password) #make_password is used to hash the password. Return the hashed password
#         super().save(*args,**kwargs)
    
#     def __str__(self):
#         return self.email

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    # password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
