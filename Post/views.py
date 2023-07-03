from django.core.cache import cache
from django.conf import settings
from .models import Post
from .serializer import PostSerializer
from .permission import IsOwnerOrReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreatePost(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            # Invalidate the cache when a new post is created
            cache.delete('post_list')
            return Response({"message": "Created", "Post": serializer.data}, status=201)

        return Response(serializer.errors, status=400)


class GetPost(GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, post_id):
        cache_key = f'post_{post_id}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data, status=200)

        try:
            post = Post.objects.get(id=post_id)
            serializer = self.serializer_class(post)
            cache.set(cache_key, serializer.data, timeout=settings.CACHE_TTL)
            return Response(serializer.data, status=200)

        except Post.DoesNotExist:
            return Response({"message": 'Post not found'}, status=400)

    def patch(self, request, post_id):
        if 'user' in request.data:
            return Response({'message': "You can't change the creator"}, status=400)

        post = Post.objects.get(id=post_id)
        if post is not None:
            self.check_object_permissions(request, post)  # Check object permissions
            serializer = self.serializer_class(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user_id=post.user_id)
                # Invalidate the cache after updating the post
                cache.delete(f'post_{post_id}')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post is not None:
            self.check_object_permissions(request, post)  # Check object permissions
            post.delete()
            # Invalidate the cache after deleting the post
            cache.delete(f'post_{post_id}')
            return Response({"message": 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class GetAll(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'post_list'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data, status=200)

        try:
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
            cache.set(cache_key, serializer.data, timeout=settings.CACHE_TTL)
            return Response(serializer.data, status=200)
        except Post.DoesNotExist:
            return Response({"message": 'Post not found'}, status=400)
