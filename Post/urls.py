from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', CreatePost.as_view()),
    path('posts/<int:post_id>', GetPost.as_view()),
    path('posts/all', GetAll.as_view()),
   

]