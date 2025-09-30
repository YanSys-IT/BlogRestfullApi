from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserProfileSerializer 


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)  
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')
    
class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)  
    comments = CommentSerializer(many=True, read_only=True)  
    comments_count = serializers.IntegerField(
        source='comments.count', read_only=True
    )  
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'content',
            'image',
            'created_at',
            'updated_at',
            'comments',
            'comments_count',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')

    


