from django.urls import path

from .views import *

urlpatterns = [
    path('users/signup/', SignUp.as_view()),
    path('users/login/', Login.as_view()),
    path('users/logout/', Logout.as_view(), name='user_logout'),
    path('users/<id>', GetUser.as_view()),

]