from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views
from .views import add_historias_to_checklist

urlpatterns = [
    #URLS relacionadas con el proyecto:
    path('', views.home, name='mP-home'),
    path('crearProyecto/', views.crearProyecto, name='crearProyecto'),

    #URLS relacionadas con el equipo:
    path('equipo/', views.equipo, name='equipo'),
    path('editarEquipo/<int:id_proyecto>/', views.editarEquipo, name='editarEquipo'),
    path('agregarMiembro/<int:id_proyecto>/<int:id_miembro>/', views.agregarMiembro, name='agregarMiembro'),
    path('eliminarMiembro/<int:id_proyecto>/<int:id_miembro>/', views.eliminarMiembro, name='eliminarMiembro'),
    path('asignarRoles/<int:id_proyecto>/', views.asignar_roles, name='asignarRoles'),
path('checklist/', views.checklist_view, name='checklist_view'),  # AGREGADO 14/11
    path('checklist/create/', views.create_checklist, name='create_checklist'),  # AGREGADO 14/11
    path('historia/<int:historia_id>/toggle_estado/', views.toggle_historia_estado, name='toggle_historia_estado'),
    path('checklist/<int:checklist_id>/add_historias/', add_historias_to_checklist, name='add_historias_to_checklist'),
    path('checklist/<int:checklist_id>/toggle_estado/', views.checklist_estado, name='toggle_checklist_estado'),

    #URLS relacionadas con el calendario:
    path('calendario/', views.calendario, name='calendario'),

    #URLS relacionadas con los riesgos
    path('riesgos/', views.riesgosProyecto, name='riesgos'),
    path('agregarRiesgo/<int:id_proyecto>/', views.agregarRiesgo, name='agregarRiesgo'),
    path('eliminarRiesgo/<int:id_riesgo>/', views.eliminarRiesgo, name='eliminarRiesgo'),

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('reportes/', views.Report, name='reportes'),
    
    path('historias/',views.historias,name='historias'),
    path('outside/', views.outside, name='outside'),
    path('proyectos/', views.lista_proyectos_usuario, name='lista_proyectos'),
    path('proyectos/', views.lista_proyectos_usuario, name='lista_proyectos'),
    path('proyectos/<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
]
