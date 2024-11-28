from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views

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
