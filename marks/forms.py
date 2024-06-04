from django import forms
from django.core.exceptions import ValidationError

from .models import Mark

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['value', 'appointment', 'student', 'feedback', 'pub_date', 'is_final']

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get("value")
        student = cleaned_data.get("student")
        is_final = cleaned_data.get("is_final")
        appointment = cleaned_data.get("appointment")

        if is_final:
            if student.received_marks.filter(appointment=appointment, is_final=True).exists():
                raise ValidationError("У этого студента уже есть итоговая оценка")
            
            if value in ['/', '+', '.', 'H']:
                raise ValidationError("Невозможно выставить такую итоговую оценку")

        return cleaned_data