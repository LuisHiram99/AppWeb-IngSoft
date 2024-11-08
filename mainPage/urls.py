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
    path('agregarMiembro/<int:id_proyecto>/', views.agregarMiembroGET, name='agregarMiembroGET'),
    path('agregarMiembro/<int:id_proyecto>/<int:id_miembro>/', views.agregarMiembro, name='agregarMiembro'),
    path('eliminarMiembro/<int:id_proyecto>/<int:id_miembro>/', views.eliminarMiembro, name='eliminarMiembro'),
    path('asignarRoles/<int:id_proyecto>/', views.asignar_roles, name='asignarRoles'),

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('reportes/', views.Report, name='reportes'),
    path('calendario/', views.calendario, name='calendario'),
    path('historias/',views.historias,name='historias'),
    path('outside/', views.outside, name='outside'),
]
