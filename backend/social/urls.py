from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MeView,PostViewSet,PeopleView,FollowView,NotificationList,MessagesView,FollowRequestsView,StoriesView,UploadConfigView
router=DefaultRouter(); router.register("posts",PostViewSet,basename="post")
urlpatterns=[path("stories/",StoriesView.as_view()),path("uploads/config/",UploadConfigView.as_view()),path("me/",MeView.as_view()),path("people/",PeopleView.as_view()),path("people/<uuid:user_id>/follow/",FollowView.as_view()),path("notifications/",NotificationList.as_view()),path("messages/",MessagesView.as_view()),path("messages/<uuid:user_id>/",MessagesView.as_view()),path("follow-requests/",FollowRequestsView.as_view()),path("follow-requests/<uuid:user_id>/",FollowRequestsView.as_view()),path("",include(router.urls))]
