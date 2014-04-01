from django import forms

from .models import People

class People(forms.ModelForm):
    class Meta:
        model = People

