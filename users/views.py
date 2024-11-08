from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from users.models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            formPH = form.save(commit=False)
            username = form.cleaned_data.get('username')
            #quite una linea de codico acá
            formPH.perfil=Profile.objects.create(first_name=form.cleaned_data.get('first_name'),
                                   last_name=form.cleaned_data.get('last_name'))
            formPH.save()
            messages.success(request, f'{username} ha sido registrado correctamente!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Tu cuenta ha sido actualizada correctamente!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.perfil)

    # Rol del usuario 
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'rol_usuario': request.user.rol,  # Obtiene el rol del usuario
    }
    return render(request, 'users/profile.html', context)

