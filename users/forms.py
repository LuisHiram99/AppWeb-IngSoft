from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
from mainPage.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(label="Correo Electrónico")

    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name','password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Correo Electrónico")

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de Usuario',
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

