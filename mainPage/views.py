from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import Reportes

def equipo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.HacerGestor()
        soyGP = request.user.SoyGestor()
        usuarios = User.objects.exclude(id=request.user.id).all()
        context={
            'soyGP': soyGP,
            'usuarios': usuarios
        }
        return render(request,'mainPage/equipo.html',context)
    else:
        redirect('login')



def Report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        area = request.POST.get('area')
        category = request.POST.get('category')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        #crear un nuevo reporte
        nuevo_reporte = Reportes(title=title, area=area, category=category, content=content, image=image)
        nuevo_reporte.save()

        return redirect("mainPage/reportes.html")

    todos_reportes = Reportes.objects.all()
    return render(request, "mainPage/reportes.html", {'reportes': todos_reportes})

def historias(request):
    return render(request,'mainPage/historias.html')
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




