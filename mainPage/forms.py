
from django import forms
from .models import Reportes,Proyecto, Miembro

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'fechaInicio',
            'fechaFin',
            'recursos_tecnologicos',
            'recurso_financiero',
            'estandares_y_plantillas',
            'reuniones_y_reportes',
        ]

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['title', 'area', 'category', 'content', 'image']

class AsignarRolForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['rol']
        labels = {'rol': 'Rol del miembro'}
        widgets = {
            'rol': forms.Select(choices=[
                (0, 'Sin asignar'),
                (1, 'Administrador'),
                (2, 'Gestor'),
                (3, 'Programador'),
            ]),
        }
