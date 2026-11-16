from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile,Post,Comment,Notification
User=get_user_model()
class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    username=serializers.RegexField(r"^[a-z0-9_]{3,32}$")
    password=serializers.CharField(write_only=True,validators=[validate_password])
    def validate_email(self,value):
        if User.objects.filter(email__iexact=value).exists(): raise serializers.ValidationError("Email already registered.")
        return value.lower()
    def validate_username(self,value):
        if Profile.objects.filter(username=value).exists(): raise serializers.ValidationError("Username already taken.")
        return value
    def create(self,data):
        user=User.objects.create_user(username=data["username"],email=data["email"],password=data["password"])
        Profile.objects.create(user=user,username=data["username"])
        return user
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=["username","full_name","bio","avatar_url","created_at"]
        read_only_fields=["created_at"]
class UserSummarySerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=["id","profile"]
class CommentSerializer(serializers.ModelSerializer):
    user=UserSummarySerializer(read_only=True)
    class Meta:
        model=Comment
        fields=["id","user","content","created_at"]
class PostSerializer(serializers.ModelSerializer):
    user=UserSummarySerializer(read_only=True)
    like_count=serializers.IntegerField(source="likes.count",read_only=True)
    comment_count=serializers.IntegerField(source="comments.count",read_only=True)
    liked_by_me=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=["id","user","media_url","caption","media_type","created_at","like_count","comment_count","liked_by_me"]
        read_only_fields=["id","user","created_at"]
    def get_liked_by_me(self,obj):
        req=self.context.get("request")
        return bool(req and req.user.is_authenticated and obj.likes.filter(user=req.user).exists())
class NotificationSerializer(serializers.ModelSerializer):
    actor=UserSummarySerializer(read_only=True)
    class Meta:
        model=Notification
        fields=["id","actor","type","post","is_read","created_at"]
