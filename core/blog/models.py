from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Blog(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(max_length=2000, null=False)
    liked_by = models.ManyToManyField(get_user_model(), through='Like', related_name='liked_blogs')
    
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    liked_blog = models.ForeignKey('Blog', related_name='likes', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"""{self.user} liked "{self.liked_blog}"."""

class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"""{self.user} commented on "{self.blog}"."""