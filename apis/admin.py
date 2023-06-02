from django.contrib import admin
from .models import Conversation
from .models import StressLevel
# Register your models here.

# admin.register(Conversation)
admin.site.register(Conversation)
admin.site.register(StressLevel)
