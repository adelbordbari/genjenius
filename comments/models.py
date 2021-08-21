import uuid

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import DateTimeField
from django.urls import reverse
from ganj.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    date = DateTimeField(auto_now_add=True)

class Note(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User, blank=True, verbose_name='Likes', related_name='note_likes')
    portion = models.CharField(max_length=500)
    body = models.TextField()
    date = DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.post.id)])

    def get_like_url(self):
        return reverse('note_like_toggle', args=[str(self.id)])

    def __str__(self):
        return self.body[:20]
