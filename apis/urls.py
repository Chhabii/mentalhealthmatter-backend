from django.urls import path, include
from . import views

urlpatterns = [
    path('predict/', views.predict_stress_level,name='predict_stress_level' ),
    path('recommend/', views.recommend,name='recommend' ),
    path("doctorai/", views.doctorai, name="doctorai"),
    path('', views.apiOverview, name="apiOverview"),
    path('blog-list/', views.blogList, name="Blogs List"),
    path('blog-detail/<str:pk>', views.blogDetail, name="Blogs Detail"),
    path('blog-create/', views.blogCreate, name="Blogs Create"),
    path('blog-update/<str:pk>', views.blogUpdate, name="Blogs Update"),
    path('blog-delete/<str:pk>', views.blogDelete, name="Blogs Delete"),


]