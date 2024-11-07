from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
from django.contrib.auth import login,logout,authenticate
from .models import Reportes,HistoriaUsuario,Proyecto,Equipo,Miembro


def equipo(request):
    if request.user.is_authenticated:
        proyectos = Proyecto.objects.filter(usuarios=request.user)
        username = request.user.username
        if request.method == 'POST':
            # Al momento de intentar acceder a los name de los inputs por medio de POST.['name_input']
            #No era posible ahcer una comparativa con los obetos proyecto, por lo tanto guarde
            #las keys del diccionario de POST.keys en un arreglo.
            #Posteriormente itere sobre los proyectos y después sobre las llaves del post.
            postkeys = request.POST.keys()
            for proyecto in proyectos:
                for key in postkeys:
                    if key == proyecto.nombre:
                        equipo = proyecto.equipo
                        break
            context={
                'hayEquipos': True,
                'equipo': equipo,
                'proyectos': proyectos,
                'username': username
            }
            return render(request,'mainPage/equipo.html',context)
        
        # usuarios = User.objects.exclude(id=request.user.id).all()
        context={
            'hayEquipos': False,
            # 'usuarios': usuarios,
            'proyectos': proyectos,
            'username': username
        }
        return render(request,'mainPage/equipo.html',context)
    else:
        redirect('login')

def agregarMiembro(request,id_proyecto,id_miembro):
    if request.user.is_authenticated:
        equipo = Proyecto.objects.get(id=id_proyecto).equipo
        if request.method == 'POST':
            usuario_miembro = User.objects.get(id=id_miembro)
            usuario_miembro.proyectos.add(Proyecto.objects.get(id=id_proyecto))
            nuevo_miembro = Miembro(
                usuario = usuario_miembro,
                rol = 0,
                equipo = equipo
            )
            nuevo_miembro.save()
            new_url = reverse('agregarMiembroGET',args=[id_proyecto])
            return redirect(new_url)
        miembros = equipo.miembros
        candidatos = User.objects.exclude(proyecto=id_proyecto)

        context = {
            'miembros': miembros,
            'id_p': id_proyecto,
            'candidatos': candidatos
        }

        return render(request,'mainPage/agregar_miembro.html',context)
    else:
        redirect('login')

def agregarMiembroGET(request,id_proyecto):
    if request.user.is_authenticated:
        equipo = Proyecto.objects.get(id=id_proyecto).equipo
        miembros = equipo.miembros
        candidatos = User.objects.exclude(proyectos=str(id_proyecto))
        context = {
            'miembros': miembros,
            'id_p': id_proyecto,
            'candidatos': candidatos,
        }

        return render(request,'mainPage/agregar_miembro.html',context)
    else:
        redirect('login')

def eliminarMiembro(request,id_proyecto,id_miembro):
    if request.user.is_authenticated:
        if request.method == 'POST':
            miembro = Miembro.objects.get(id=id_miembro)
            usuario = miembro.usuario
            usuario.proyectos.remove(id_proyecto)
            miembro.delete()
        new_url = reverse('agregarMiembroGET',args=[id_proyecto])
        return redirect(new_url)
    else:
        redirect('login')

def asignarRoles(request):
    if request.user.is_authenticated:
        return render(request,'mainPage/asignar_roles.html')
    else:
        redirect('login')

def Report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        area = request.POST.get('area')
        category = request.POST.get('category')
        content = request.POST.get('content')
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

        return render(request, "mainPage/reportes.html", {
            'reportes': reportes_list,
            'usuario_actual': request.user
        })

def historias(request):
    return render(request,'mainPage/historias.html')
def home (request):
    if request.user.is_authenticated:
        return render(request, 'mainPage/home.html')
    else:
            return redirect('outside')

def crearProyecto(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get("nombre-proyecto")
            fi = request.POST.get("fecha-inicio")
            ff = request.POST.get("fecha-fin")
            equipo =  Equipo(nombre="placeholder")
            equipo.save()
            miembro = Miembro(usuario=request.user,rol=0,equipo=equipo)
            miembro.save()

            nuevo_proyecto = Proyecto(
                nombre=nombre,
                fechaInicio=fi,
                fechaFin=ff,
                equipo=equipo,
                gestorProyecto=request.user
            )

            nuevo_proyecto.save()
            request.user.proyectos.add(nuevo_proyecto)
            return redirect("equipo")
        else:
            return render(request,'mainPage/crear_proyecto.html')
    else:
        return redirect('login')

def outside (request):
    return render(request, 'mainPage/outside.html')

def calendario(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=request.user.username)
        eventos = HistoriaUsuario.objects.filter(miembroAsignado=usuario)
        context = {
        "eventos": eventos
        }
        return render(request,'mainPage/calendario.html',context)
    else:
        return redirect('login')




