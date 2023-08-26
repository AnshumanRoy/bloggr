from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from authentication.serializers import UserProfileSerializer, time_ago

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    
    user = UserProfileSerializer()
    time_since_posted = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('user', 'content', 'time_since_posted')
    
    def get_time_since_posted(self, obj):
        return time_ago(obj.timestamp)
    
    def get_comments_queryset(self, obj):
        return obj.comments.order_by('-timestamp')
        
class GetBlogSerializer(serializers.ModelSerializer):
    
    author = UserProfileSerializer()
    liked_count = serializers.SerializerMethodField(read_only=True)
    time_since_posted = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Blog
        fields = (
            'author',
            'liked_count',
            'edited',
            'time_since_posted',
            'title',
            'content',
            'comments',
        )
    
    def get_liked_count(self, obj):
        return obj.liked_by.count()
    
    def get_time_since_posted(self, obj):
        return time_ago(obj.created_on)
        
class ListBlogSerializer(serializers.ModelSerializer):
    
    link = serializers.HyperlinkedIdentityField(view_name='get-blog-by-id', read_only=True)
    liked_by_count = serializers.SerializerMethodField(read_only=True)
    author = UserProfileSerializer()
    time_since_posted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = (
            'author', 
            'title', 
            'liked_by_count',
            'edited',
            'link',
            'time_since_posted',
        )
    
    def get_liked_by_count(self, obj):
        return obj.liked_by.count()
    
    def get_time_since_posted(self, obj):
        return time_ago(obj.created_on)

class CreateBlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = (
            'title',
            'content',
        )
        kwargs = {
            'title':{'required':True},
            'content':{'required':True},
        }

class UpdateBlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = (
            'title',
            'content',
        )
    
    def validate(self, attrs):
        if not (attrs['title'] or attrs['content']):
            raise serializers.ValidationError({"message": {"No edits made."}})
        return super().validate(attrs)
    