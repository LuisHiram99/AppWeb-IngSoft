from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('profile/',user_views.profile, name='profile'),
    path('', include('mainPage.urls')),

]
