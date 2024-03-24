from django.shortcuts import render
from django.contrib.auth.views import LoginView as LV
from .forms import LoginForm
from django.urls import reverse_lazy

# Create your views here.

class LoginView(LV):
    form_class = LoginForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('users:login')