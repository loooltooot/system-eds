from django.shortcuts import render
from django.contrib.auth.views import LoginView as LV
from .forms import LoginForm

# Create your views here.

class LoginView(LV):
    form_class = LoginForm
    template_name = 'users/login.html'