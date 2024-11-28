
from django import forms
from .models import Reportes, Proyecto, Miembro, Checklist, HistoriaUsuario


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

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['name', 'historias']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del checklist'}),
            'historias': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
historias = forms.ModelMultipleChoiceField(
        queryset=HistoriaUsuario.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
