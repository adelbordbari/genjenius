from django.urls import reverse
from django.db import models
from django.db.models.fields import DateTimeField
from ganj.models import Post
from django.contrib.auth.models import User

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = DateTimeField(auto_now_add=True)

class Note(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="note_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portion = models.CharField(max_length=500)
    body = models.TextField()
    date = DateTimeField(auto_now_add=True)
