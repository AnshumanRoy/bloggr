from django.urls import path
from .views import GetUpdateDeleteBlogView, ListBlogView, CreateBlogView

urlpatterns = [
    path("<int:pk>/", GetUpdateDeleteBlogView.as_view(), name='get-blog-by-id'),
    path("", ListBlogView.as_view(), name='list-blogs'),
    path("create/", CreateBlogView.as_view(), name='create-blog'),
]
