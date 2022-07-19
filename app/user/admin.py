from django.contrib import admin
from django.contrib.auth import get_user_model
from app.user.models import Profile, FollowUnfollow

User = get_user_model()

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(FollowUnfollow)
