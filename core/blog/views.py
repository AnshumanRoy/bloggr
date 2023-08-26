from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import GetBlogSerializer

class GetUpdateDeleteBlogView(APIView):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        if blog:
            serializer = GetBlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        blog = Blog.objects.get(id=pk)
        if blog:
            if blog.author == request.user:
                serializer = UpdateBlogSerializer(blog, data=request.data)
                if serializer.is_valid():
                    serializer.save(edited=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        blog = Blog.objects.get(id=pk)
        if blog:
            if blog.author == request.user:
                blog.delete()
                return Response({"message": "Object deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ListBlogView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = ListBlogSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateBlogView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        serializer = CreateBlogSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(author=user)
            blog_id = instance.id
            blog_url = reverse('get-blog-by-id', kwargs={'pk': blog_id})
            return HttpResponseRedirect(blog_url)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)