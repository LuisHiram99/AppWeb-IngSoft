# forms.py
from django import forms
from .models import Reportes

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['title', 'area', 'category', 'content', 'image']
