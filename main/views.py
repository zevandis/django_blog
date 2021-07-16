from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, HttpResponse

from .models import Post, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm, CreatePostForm



class PostsList(ListView):

    paginate_by = 6
    model = Post
    queryset = Post.objects.all()
    template_name = 'main/home.html'


class PostDetail(View):

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        last_posts = Post.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'main/post_detail.html', context={
            'post': post,
            'last_posts': last_posts,
            'comment_form': comment_form
        })

    def post(self, request, pk, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            post = Post.objects.get(id=pk)
            user = self.request.user
            comment = Comment.objects.create(post=post, text=text, user=user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'main/post_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'main/signup.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/signup.html', context={
            'form': form
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'main/signin.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/signin.html', context={
            'form': form
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'main/contact.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}   {from_email}', message, from_email, ['reppair1@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'main/contact.html', context={
            'form': form
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/success.html', context={
            'title': 'Спасибо'
        })


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        result = ''
        if query:
            result = Post.objects.filter(
                Q(h1__icontains=query) | Q(text__icontains=query)
            )
        paginator = Paginator(result, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'main/search.html', context={
            'result': page_obj,
            'count': paginator.count
        })


class CreatePostView(View):
    def get(self, request, *args, **kwargs):
        create_form = CreatePostForm()
        return render(request, 'main/create_post.html', context={
            'create_form': create_form
        })

    def post(self, request, *args, **kwargs):
        create_form = CreatePostForm(request.POST, request.FILES)
        if create_form.is_valid():
            print(request.POST, request.FILES)
            h1 = request.POST['h1']
            title = request.POST['title']
            description = request.POST['description']
            url = request.POST['url']
            text = request.POST['text']
            image = request.FILES['image']
            author = self.request.user
            post = Post.objects.create(
                h1=h1,
                title=title,
                description=description,
                url=url,
                text=text,
                author=author,
                image=image
            )
            return HttpResponseRedirect('/')
        return render(request, 'main/create_post.html', context={
            'create_form': create_form
        })