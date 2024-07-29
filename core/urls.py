from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('chat/', views.chat, name='chat'),
    path('logout/', views.logout_user, name='logout'),
    path('respond/', views.respond_chat, name='respond'),
    path('respond_view/', views.respond_view, name='respond_view')
]