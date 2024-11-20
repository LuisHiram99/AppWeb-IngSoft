from django.contrib import admin
from .models import User,Reportes,Proyecto,HistoriaUsuario,Miembro,Equipo

admin.site.register(Miembro)
admin.site.register(Equipo)
admin.site.register(HistoriaUsuario)
admin.site.register(Proyecto)
admin.site.register(User)
admin.site.register(Reportes)

# Register your models here.
