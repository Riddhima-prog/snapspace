from django.contrib.auth import get_user_model
from rest_framework import generics,permissions,status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile,Post,Like,Comment,Follow,Notification
from .serializers import RegisterSerializer,ProfileSerializer,PostSerializer,CommentSerializer,NotificationSerializer
from .permissions import IsOwnerOrReadOnly
User=get_user_model()
class HealthView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request): return Response({"status":"ok","service":"snapspace-api"})
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[permissions.AllowAny]
class MeView(APIView):
    def get(self,request): return Response(ProfileSerializer(request.user.profile).data)
    def patch(self,request):
        ser=ProfileSerializer(request.user.profile,data=request.data,partial=True); ser.is_valid(raise_exception=True); ser.save()
        return Response(ser.data)
class PostViewSet(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly]
    queryset=Post.objects.select_related("user","user__profile").all()
    http_method_names=["get","post","delete","head","options"]
    def perform_create(self,serializer): serializer.save(user=self.request.user)
    @action(detail=True,methods=["post"])
    def like(self,request,pk=None):
        post=self.get_object(); _,created=Like.objects.get_or_create(user=request.user,post=post)
        if created and post.user_id!=request.user.id: Notification.objects.create(recipient=post.user,actor=request.user,type="like",post=post)
        return Response({"liked":True})
    @action(detail=True,methods=["delete"])
    def unlike(self,request,pk=None):
        Like.objects.filter(user=request.user,post=self.get_object()).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True,methods=["get","post"])
    def comments(self,request,pk=None):
        post=self.get_object()
        if request.method=="GET": return Response(CommentSerializer(post.comments.select_related("user","user__profile"),many=True).data)
        ser=CommentSerializer(data=request.data); ser.is_valid(raise_exception=True)
        comment=Comment.objects.create(post=post,user=request.user,**ser.validated_data)
        if post.user_id!=request.user.id: Notification.objects.create(recipient=post.user,actor=request.user,type="comment",post=post)
        return Response(CommentSerializer(comment).data,status=status.HTTP_201_CREATED)
class PeopleView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]; serializer_class=ProfileSerializer
    def get_queryset(self): return Profile.objects.exclude(user=self.request.user).filter(username__icontains=self.request.query_params.get("q","")).order_by("username")[:100]
class FollowView(APIView):
    def post(self,request,user_id):
        if str(request.user.id)==str(user_id): return Response({"detail":"You cannot follow yourself."},status=400)
        target=generics.get_object_or_404(User,pk=user_id)
        Follow.objects.get_or_create(follower=request.user,following=target)
        Notification.objects.get_or_create(recipient=target,actor=request.user,type="follow",post=None)
        return Response({"following":True})
    def delete(self,request,user_id):
        Follow.objects.filter(follower=request.user,following_id=user_id).delete()
        return Response(status=204)
class NotificationList(generics.ListAPIView):
    serializer_class=NotificationSerializer
    def get_queryset(self): return Notification.objects.filter(recipient=self.request.user).select_related("actor","actor__profile")[:100]
