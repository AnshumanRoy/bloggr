from django.contrib import admin
from .models import Blog, Like, Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(Like)
admin.site.register(Comment)