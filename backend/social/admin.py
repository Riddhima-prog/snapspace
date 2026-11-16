from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile,Post,Like,Comment,Follow,Notification,Story
admin.site.register(User,UserAdmin)
for model in [Profile,Post,Like,Comment,Follow,Notification,Story]: admin.site.register(model)
