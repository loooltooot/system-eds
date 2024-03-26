from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as LV
from .forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

class LoginView(LV):
    form_class = LoginForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('marks:index')
    
@login_required
def logout_user(request):
    logout(request)
    return redirect('users:login')