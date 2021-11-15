from django.contrib import admin

from .models import User, Post, Photo, Comment


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Comment)
