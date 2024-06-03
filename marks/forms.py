from django import forms

from .models import Mark

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['value', 'appointment', 'student', 'feedback', 'pub_date', 'is_final']
