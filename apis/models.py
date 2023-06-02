from django.db import models
from accounts.models import User
class Conversation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='conversations',null=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __str__(self):
        return self.user_message


class StressLevel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stress_level',null=True)
    level = models.IntegerField()
    measured_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.level}"
