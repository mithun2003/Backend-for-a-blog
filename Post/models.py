from django.db import models
from User.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    
    