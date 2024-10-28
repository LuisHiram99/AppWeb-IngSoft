from django.contrib import admin
from .models import User,Reportes,Proyecto,HistoriaUsuario,CriterioAceptacion

admin.site.register(CriterioAceptacion)
admin.site.register(HistoriaUsuario)
admin.site.register(Proyecto)
admin.site.register(User)
admin.site.register(Reportes)

# Register your models here.
