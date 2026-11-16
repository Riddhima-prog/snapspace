import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email=models.EmailField(unique=True)
    REQUIRED_FIELDS=["email"]
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    username=models.CharField(max_length=32,unique=True)
    full_name=models.CharField(max_length=60,blank=True)
    bio=models.CharField(max_length=250,blank=True)
    avatar_url=models.URLField(blank=True)
    is_private=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"@{self.username}"
class Post(models.Model):
    MEDIA_TYPES=[("image","Image"),("video","Video")]
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    media_url=models.URLField(max_length=2048)
    caption=models.CharField(max_length=2200,blank=True)
    media_type=models.CharField(max_length=5,choices=MEDIA_TYPES,default="image")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=["user","post"],name="unique_user_post_like")]
class Comment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    content=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["created_at"]
class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following_edges")
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower_edges")
    status=models.CharField(max_length=10,choices=[("pending","Pending"),("accepted","Accepted")],default="accepted")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["follower","following"],name="unique_follow_edge"),models.CheckConstraint(condition=~models.Q(follower=models.F("following")),name="prevent_self_follow")]
class Notification(models.Model):
    TYPES=[("like","Like"),("comment","Comment"),("follow","Follow")]
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    actor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_notifications")
    type=models.CharField(max_length=10,choices=TYPES)
    post=models.ForeignKey(Post,null=True,blank=True,on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]


class DirectMessage(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_direct_messages")
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name="received_direct_messages")
    content=models.CharField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    read_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        ordering=["created_at"]
        indexes=[models.Index(fields=["sender","recipient","created_at"]),models.Index(fields=["recipient","sender","created_at"])]


def story_expiry():
    return timezone.now() + timedelta(hours=24)


class Story(models.Model):
    MEDIA_TYPES = [("image", "Image"), ("video", "Video")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    media_url = models.URLField(max_length=2048)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    caption = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=story_expiry, db_index=True)

    class Meta:
        ordering = ["created_at"]
