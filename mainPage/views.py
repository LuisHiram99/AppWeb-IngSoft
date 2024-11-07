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
        doc = request.FILES.get('doc')

        if request.user.is_authenticated:
            Reportes.objects.create(
                user=request.user,
                title=title,
                area=area,
                category=category,
                content=content,
                image=image,
                doc=doc
            )
            return redirect('reportes')

    filter_category = request.GET.get('filter_category')

    if filter_category:
        reportes_list = Reportes.objects.filter(category=filter_category, user=request.user)
    else:
        reportes_list = Reportes.objects.filter(user=request.user)

    return render(request, 'reportes.html', {
        'reportes': reportes_list,
        'usuario_actual': request.user
    })


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




