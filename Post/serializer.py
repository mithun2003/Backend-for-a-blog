from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()
    class Meta:
        model = Post
        exclude = ['post_date']