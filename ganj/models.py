import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from slugify import slugify_unicode


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unicode(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Title')
    body = models.TextField(null=False, verbose_name='Body')
    posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, blank=True, verbose_name='Likes', related_name='post_likes')
    author = models.CharField(max_length=100, verbose_name='Author', default='', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags', default=None, blank=True)

    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.id)])

    def get_like_url(self):
        return reverse('like_toggle', args=[str(self.id)])

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    


class Stream(models.Model):
    following = models.ForeignKey(
        User, related_name='stream_following', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        # user = me. get all my followers
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower,
                            date=post.posted, following=user)
            stream.save()


post_save.connect(Stream.add_post, sender=Post)
