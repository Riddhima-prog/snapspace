from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MeView,PostViewSet,PeopleView,FollowView,NotificationList
router=DefaultRouter(); router.register("posts",PostViewSet,basename="post")
urlpatterns=[path("me/",MeView.as_view()),path("people/",PeopleView.as_view()),path("people/<uuid:user_id>/follow/",FollowView.as_view()),path("notifications/",NotificationList.as_view()),path("",include(router.urls))]
