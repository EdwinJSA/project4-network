from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


''' that's for the posts '''
class newPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} posted: {self.content} on {self.date}"
    
''' this models is for keep the control of followers'''
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    def __str__(self):
        return f"{self.user} followed: {self.follower}"