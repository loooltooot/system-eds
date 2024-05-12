from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User

class LoginForm(AuthenticationForm):
    def __init__(self, request: Any = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Номер телефона'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'

    class Meta:
        model = User