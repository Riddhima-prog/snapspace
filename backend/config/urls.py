from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from social.auth import EmailOrUsernameTokenView
from social.views import RegisterView, HealthView
urlpatterns=[path("admin/",admin.site.urls),path("api/health/",HealthView.as_view()),path("api/auth/register/",RegisterView.as_view()),path("api/auth/token/",EmailOrUsernameTokenView.as_view()),path("api/auth/token/refresh/",TokenRefreshView.as_view()),path("api/",include("social.urls"))]
