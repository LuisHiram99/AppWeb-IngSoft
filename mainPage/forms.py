
from django import forms
from .models import Reportes,Proyecto

class ProyectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'fechaInicio', 'fechaFin']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['title', 'area', 'category', 'content', 'image']
