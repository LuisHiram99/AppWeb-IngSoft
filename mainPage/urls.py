from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views

urlpatterns = [
    path('', views.home, name='mP-home'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('equipo/', views.equipo, name='equipo'),
    path('reportes/', views.Report, name='reportes'),
    path('calendario/', views.calendario, name='calendario'),
    path('historias/',views.historias,name='historias'),
    path('outside/', views.outside, name='outside'),
]
