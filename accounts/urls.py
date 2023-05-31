from django.urls import path
from . import views

urlpatterns = [
    path('api_register/',views.api_register,name='api_register'),
    path('api_login/',views.api_login,name='api_login'),
    path("api_logout/",views.api_logout,name='api_logout'),
]

