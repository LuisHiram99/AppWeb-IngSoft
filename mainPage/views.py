from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate

def equipo(request):
    return render(request,'mainPage/equipo.html')

def reportes(request):
    return render(request,'mainPage/reportes.html')

def hu(request):
    return render(request,'mainPage/hu.html')
def home (request):
    return render(request, 'mainPage/home.html')
def outside (request):
    return render(request, 'mainPage/outside.html')

def calendario(request):
    if request.user.is_authenticated:
        fei = request.user.ObtenerFI()
        fef = request.user.ObtenerFF()
        print(fei)
        context = {
            "fi": fei,
            "ff": fef
            }
        return render(request,'mainPage/calendario.html',context)
    else:
        return redirect('login')




