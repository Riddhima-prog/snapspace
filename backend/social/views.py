from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
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
class DemoLoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        # Shared public demo account: convenient for trying the app without signup.
        user,created=User.objects.get_or_create(
            username="snapspace_demo",
            defaults={"email":"demo@snapspace.local","is_active":True},
        )
        if created:
            user.set_password(get_random_string(48))
            user.save()
        Profile.objects.get_or_create(user=user,defaults={"username":"snapspace_demo","full_name":"SnapSpace Demo"})
        refresh=RefreshToken.for_user(user)
        return Response({"refresh":str(refresh),"access":str(refresh.access_token)})

class PasswordResetRequestView(APIView):
    permission_classes=[permissions.AllowAny]
    throttle_scope="anon"
    def post(self,request):
        email=(request.data.get("email") or "").strip()
        # Always return the same response to avoid revealing registered emails.
        user=User.objects.filter(email__iexact=email,is_active=True).first() if email else None
        if user:
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            reset_url=request.build_absolute_uri("/?reset_uid="+uid+"&reset_token="+token)
            send_mail(
                "Reset your SnapSpace password",
                "Use this one-time link to choose a new password. It expires automatically:\n\n"+reset_url+"\n\nIf you did not request this, ignore this email.",
                None,[user.email],fail_silently=False,
            )
        return Response({"detail":"If an account exists for that email, password reset instructions have been sent."})

class PasswordResetConfirmView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        uid=request.data.get("uid","")
        token=request.data.get("token","")
        password=request.data.get("password","")
        try:
            user=User.objects.get(pk=force_str(urlsafe_base64_decode(uid)),is_active=True)
        except (User.DoesNotExist,ValueError,TypeError,OverflowError):
            return Response({"detail":"This reset link is invalid or has expired. Request a new one."},status=400)
        if not default_token_generator.check_token(user,token):
            return Response({"detail":"This reset link is invalid or has expired. Request a new one."},status=400)
        try:
            password_validation.validate_password(password,user)
        except Exception as exc:
            return Response({"password":list(exc.messages)},status=400)
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response({"detail":"Password updated. You can now log in."})

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
