from django.contrib import admin
from .models import User, newPost, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(newPost)
admin.site.register(Follow)