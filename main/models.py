from django.db import models
from django.utils import timezone


class Post(models.Model):

    h1 = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.SlugField()
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
