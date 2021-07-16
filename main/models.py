from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):

    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = models.TextField(blank=True)
    text = models.TextField()
    image = models.ImageField(blank=True, upload_to='media')
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    tag = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.text
