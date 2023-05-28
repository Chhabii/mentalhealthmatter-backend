from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer
from .models import Blog
# Create your views here.


############ BLOG ###############3
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/blog/blog-list/',
        'Detail view': '/blog/blog-detail/<str:pk>/',
        'Create': '/blog/blog-create/',
        'Update': '/blog/blog-update/<str:pk>',
        'Delete': '/blog/blog-delete/<str:pk>',
    }

    return Response(api_urls)

@api_view(['GET'])
def blogList(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def blogDetail(request, pk):
    try:
        blogs = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blogs, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def blogCreate(request):
    
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def blogUpdate(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(instance=blog, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def blogDelete(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    blog.delete()
    return Response("Blog successfully deleted!!!")



