from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(unique=True,null=False,blank=False)
    password = models.CharField(max_length=255,null=False,blank=False)

    def save(self,*args,**kwargs):
        self.password = make_password(self.password) #make_password is used to hash the password. Return the hashed password
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.email