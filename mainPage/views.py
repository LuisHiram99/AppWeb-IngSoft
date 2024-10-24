from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import Proyecto,HistoriaUsuario,Reportes


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
        title = request.POST['title']
        area = request.POST['area']
        category = request.POST['category']
        content = request.POST['content']
        image = request.FILES.get('image')

        nuevo_reporte = Reportes.objects.create(
            title=title,
            area=area,
            category=category,
            content=content,
            image=image
        )

        reportes_list = Reportes.objects.all()
        return render(request, 'reportes.html', {'reportes': reportes_list})

    reportes_list = Reportes.objects.all()
    return render(request, 'reportes.html', {'reportes': reportes_list})


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




