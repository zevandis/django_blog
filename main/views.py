from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Post


class PostsList(ListView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'main/home.html'


class PostDetail(DetailView):

    model = Post
    slug_field = 'id'
    template_name = 'main/post_detail.html'
