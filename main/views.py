from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, HttpResponse

from .models import Post
from .forms import SignUpForm, SignInForm, FeedBackForm



class PostsList(ListView):

    paginate_by = 6
    model = Post
    queryset = Post.objects.all()
    template_name = 'main/home.html'


class PostDetail(DetailView):

    model = Post
    slug_field = 'id'
    template_name = 'main/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['last_posts'] = Post.objects.all().order_by('-id')[:5]
        return context


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