from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostsList.as_view(), name='home'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('contact/', views.FeedBackView.as_view(), name='contact'),
    path('contact/success/', views.SuccessView.as_view(), name='success'),
    path('search/', views.SearchView.as_view(), name='search')
]