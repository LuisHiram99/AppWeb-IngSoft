from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.decorators.http import require_POST
User = get_user_model()
from .models import Reportes, HistoriaUsuario, Proyecto, Equipo, Miembro, RiesgoProyecto, Checklist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AsignarRolForm, ProyectoForm, ChecklistForm
from django.http import HttpResponseForbidden, JsonResponse


def riesgosProyecto(request):
    if request.user.is_authenticated:
        proyectos = Proyecto.objects.filter(usuarios=request.user)
        username = request.user.username
        if request.method == 'POST':
            # Al momento de intentar acceder a los name de los inputs por medio de POST.['name_input']
            #No era posible ahcer una comparativa con los obetos proyecto, por lo tanto guarde
            #las keys del diccionario de POST.keys en un arreglo.
            #Posteriormente itere sobre los proyectos y después sobre las llaves del post.
            postkeys = request.POST.keys()
            hayRiesgos = False
            for proyecto in proyectos:
                for key in postkeys:
                    if key == proyecto.nombre:
                        proyecto_contx = proyecto
                        riesgos = RiesgoProyecto.objects.filter(id=proyecto.id)
                        id_proyecto = proyecto.id
                        if RiesgoProyecto.objects.filter(id=proyecto.id).count() != 0:
                            hayRiesgos = True
                        break
            context={
                    'proyecto': proyecto_contx,
                    'id_proyecto': id_proyecto,
                    'hayProyectos': True,
                    'hayRiesgos': hayRiesgos,
                    'riesgos': riesgos,
                    'proyectos': proyectos,
                    'username': username
            }
            return render(request,'mainPage/riesgos.html',context)
            
        context={
                'hayProyectos': False,
                'proyectos': proyectos,
                'username': username
        }
        return render(request,'mainPage/riesgos.html',context)
    else:
        redirect('login')

def agregarRiesgo(request,id_proyecto):
    if request.user.is_authenticated:
        if request.method == 'POST':
            proyecto = Proyecto.objects.get(id=id_proyecto)
            titulo = request.POST.get("titulo-riesgo")
            descripcion = request.POST.get("descripcion-riesgo")
            gravedad = request.POST.get("gravedad-riesgo")

            nuevo_riesgo = RiesgoProyecto(
                Titulo = titulo,
                descripcion = descripcion,
                gravedad = gravedad,
                proyecto = proyecto
            )

            nuevo_riesgo.save()
            return redirect('riesgos')

        context = {
            'id_p': id_proyecto,
        }
        return render(request,'mainPage/agregar_riesgos.html',context)
    else:
        redirect('login')

def eliminarRiesgo(request,id_riesgo):
    if request.user.is_authenticated:
        riesgo = RiesgoProyecto.objects.get(id=id_riesgo)
        riesgo.delete()
        return redirect('riesgos')
    else:
        redirect('login')

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
            new_url = reverse('editarEquipo',args=[id_proyecto])
            return redirect(new_url)
        miembros = equipo.miembros
        candidatos = User.objects.exclude(proyecto=id_proyecto)

        context = {
            'miembros': miembros,
            'id_p': id_proyecto,
            'candidatos': candidatos
        }
        return render(request,'mainPage/editar_equipo.html',context)
    else:
        redirect('login')

def editarEquipo(request,id_proyecto):
    if request.user.is_authenticated:
        equipo = Proyecto.objects.get(id=id_proyecto).equipo
        miembros = equipo.miembros
        candidatos = User.objects.exclude(proyectos=str(id_proyecto))
        context = {
            'miembros': miembros,
            'id_p': id_proyecto,
            'candidatos': candidatos,
        }

        return render(request,'mainPage/editar_equipo.html',context)
    else:
        redirect('login')

def eliminarMiembro(request,id_proyecto,id_miembro):
    if request.user.is_authenticated:
        if request.method == 'POST':
            miembro = Miembro.objects.get(id=id_miembro)
            usuario = miembro.usuario
            usuario.proyectos.remove(id_proyecto)
            miembro.delete()
        new_url = reverse('editarEquipo',args=[id_proyecto])
        return redirect(new_url)
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
    # if request.user.is_authenticated:
    #     #Si recibí una petición post
    #     if request.method == 'POST':
    #         titulo = request.POST.get("titulo")
    #         descripcion = request.POST.get("descripcion")
    #         feIni = request.POST.get("feIni")
    #         feFin = request.POST.get("feFin")
    #         rol = request.POST.get("rol")
    #         id_proyecto = request.POST.get("proyecto-id")

    #         #Con el id del proyecto seleccionado en el forms, obtenemos el proyecto y los miembros en el
    #         #que cumplen con el rol seleccionado
    #         proyecto = Proyecto.objects.get(id=id_proyecto)
    #         # el atributo de filter: equipo__proyecto es parecido a un puntero de c++:
    #         # dame todos los miembros que tienen un proyecto igual a <objeto_proyecto>
    #         miembros = Miembro.objects.filter(rol=rol).filter(equipo__proyecto=proyecto)
            
    #         #Creamos un objeto que guarde los datos recibidos por el forms
    #         nueva_historia = HistoriaUsuario(
    #             nombre = titulo,
    #             fechaInicio = feIni,
    #             fechaFin = feFin,
    #             descripcion = descripcion,
    #             proyecto = proyecto
    #         )
    #         #guardamos el objeto en la base de datos
    #         nueva_historia.save()
            
    #         #agregamos los miembros a la base de datos uno por uno, ya que add no puede agregar un queryset
    #         for miembro in miembros:
    #             nueva_historia.miembroAsignado.add(miembro)
    #         nueva_historia.save()


    #         return redirect('historias')
    #     else:
    #         #Le mandamos solo los proyectos en los que el usuario actual es gestor de proyecto.
    #         proyectos = Proyecto.objects.filter(gestorProyecto=request.user)
    #         context = {
    #             'proyectos': proyectos
    #         }
    #         return render(request,'mainPage/historias.html',context)
    # else:
    #     return redirect('login')
    
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
            equipo =  Equipo(nombre=nombre)
            equipo.save()
            miembro = Miembro(usuario=request.user,rol=2,equipo=equipo)
            miembro.save()

            control_versiones = request.POST.get("control-versiones")
            editores_codigo = request.POST.get("editores-codigo")
            hardware = request.POST.get("hardware")
            herramientas_prueba = request.POST.get("herramientas-prueba")
            canal_comunicacion = request.POST.get("canal-comunicacion")
            recurso_financiero = request.POST.get("recurso-financiero")
            estandares_plantillas = request.POST.get("estandares-plantillas")
            frecuencia_reuniones = request.POST.get("frecuencia-reuniones")
            entrega_reportes = request.POST.get("entrega-reportes")

            nuevo_proyecto = Proyecto(
                nombre=nombre,
                fechaInicio=fi,
                fechaFin=ff,
                equipo=equipo,
                gestorProyecto=request.user,
                recursos_tecnologicos=f"Control de versiones: {control_versiones}\nEditores: {editores_codigo}\nHardware: {hardware}\nHerramientas de prueba: {herramientas_prueba}\nCanal de comunicación: {canal_comunicacion}",
                recurso_financiero=recurso_financiero,
                estandares_y_plantillas=estandares_plantillas,
                reuniones_y_reportes=f"Frecuencia: {frecuencia_reuniones}\nEntrega: {entrega_reportes}",
            )

            nuevo_proyecto.save()
            request.user.proyectos.add(nuevo_proyecto)

            return redirect("lista_proyectos")
        else:
            return render(request,'mainPage/crear_proyecto.html')
    else:
        return redirect('login')
    
def lista_proyectos_usuario(request):
    """
    Vista que lista todos los proyectos donde el usuario es parte.
    """
    proyectos = Proyecto.objects.filter(gestorProyecto=request.user)
    return render(request, 'mainPage/lista_proyectos.html', {'proyectos': proyectos})

def detalle_proyecto(request, proyecto_id):
    """
    Vista que muestra los detalles de un proyecto.
    """
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    return render(request, 'mainPage/detalle_proyecto.html', {'proyecto': proyecto})

def outside (request):
    return render(request, 'mainPage/outside.html')

def calendario(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id_proyecto = request.POST.get("filtro-proyecto")
            num_rol = request.POST.get("filtro-rol","-1")
            estado_filtro = request.POST.get("filtro-estado")

            if id_proyecto == "-1":
                proyecto_filtro = None
            else:
                proyecto_filtro = Proyecto.objects.get(id=id_proyecto)

            #si el proyecto no se filtro entonces:
            if proyecto_filtro == None:
                eventos = HistoriaUsuario.objects.filter(miembroAsignado__usuario=request.user)
            #Si se filtro un proyecto y soy su gestor de proyecto entonces:
            elif proyecto_filtro != None and proyecto_filtro.gestorProyecto == request.user:
                #Si además agregué un filtro de rol entonces:
                if num_rol != "-1" or None:
                    eventos = HistoriaUsuario.objects.filter(proyecto=proyecto_filtro).filter(miembroAsignado__rol=str(num_rol))  
                else: 
                    eventos = HistoriaUsuario.objects.filter(proyecto=proyecto_filtro)
            #Solo se muestran las historias del usuario que hizó la petición
            else:
                eventos = HistoriaUsuario.objects.filter(proyecto=proyecto_filtro).filter(miembroAsignado__usuario=request.user)

            #Si no se solicitaron todas las tareas, se filtra por estado completado o sin completar:
            if estado_filtro != "-1":
                eventos = eventos.filter(estado=estado_filtro)

            print("filtro estado: " + estado_filtro)
            proyectos = Proyecto.objects.filter(usuarios=request.user.id)
            context = {
                "eventos": eventos,
                "proyectos": proyectos,
                "proyFiltro": proyecto_filtro
            }
            redirect("calendario")
        else:
            eventos = HistoriaUsuario.objects.filter(miembroAsignado__usuario=request.user)
            proyecto_filtro = None
            proyectos = Proyecto.objects.filter(usuarios=request.user.id)
            context = {
                "eventos": eventos,
                "proyectos": proyectos,
                "proyFiltro": proyecto_filtro
            }
        return render(request,'mainPage/calendario.html',context)
    else:
        return redirect('login')

@login_required
def asignar_roles(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)

    # Verificar si el usuario es el gestor del proyecto
    if request.user != proyecto.gestorProyecto:
        messages.warning(request, "No tienes permisos para asignar roles en este proyecto.")
        return redirect('mP-home')  # Redirigir a la página de inicio si no es el gestor

    equipo = proyecto.equipo
    miembros = equipo.miembros.all()  # Lista de miembros del equipo

    if request.method == 'POST':
        form = AsignarRolForm(request.POST)

        # Verificar si el formulario es válido y que el usuario siga siendo el gestor
        if form.is_valid() and request.user == proyecto.gestorProyecto:
            #El equipo no puede quedarse sin gestor,, agregar pruebas sobre esto
            miembro_id = request.POST.get("miembro_id")
            miembro = Miembro.objects.get(id=miembro_id)
            miembro.rol = form.cleaned_data['rol']
            miembro.save()
            #Si se creo un nuevo gestor entonces y este es distinto al usuario original:
            if miembro.rol == 2 and proyecto.gestorProyecto != miembro.usuario: 
                ex_gestor = Miembro.objects.filter(equipo__proyecto=id_proyecto).get(usuario=proyecto.gestorProyecto)
                ex_gestor.rol = 0
                ex_gestor.save() 
                proyecto.gestorProyecto = miembro.usuario 
                proyecto.save()
                


            messages.success(request, f"Rol de {miembro.usuario.username} actualizado correctamente.")
            return redirect('asignarRoles', id_proyecto=id_proyecto)
    else:
        form = AsignarRolForm()

    context = {
        'form': form,
        'miembros': miembros,
        'proyecto': proyecto,
    }
    return render(request, 'mainPage/asignar_roles.html', context)

@login_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verifica si el usuario es el gestor del equipo
    if proyecto.gestorProyecto != request.user:
        return HttpResponseForbidden("No tienes permisos para editar este proyecto.")

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('detalle_proyecto', proyecto_id=proyecto.id)
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'mainPage/editar_proyecto.html', {'form': form, 'proyecto': proyecto})

@login_required
def create_checklist(request):
    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST)
        if checklist_form.is_valid():
            checklist = checklist_form.save(commit=False)
            checklist.user = request.user
            checklist.save()
            checklist_form.save_m2m()  
            messages.success(request, "Checklist creado exitosamente.")
            return redirect('checklist_view')
    else:
        checklist_form = ChecklistForm()

    return render(request, 'mainPage/create_checklist.html', {'checklist_form': checklist_form})


@login_required
def checklist_view(request):
    checklists = Checklist.objects.filter(user=request.user)

    # Maneja el formulario de notas
    if request.method == 'POST':
        historia_id = request.POST.get('historia_id')
        nota = request.POST.get('nota')

        try:
            historia = HistoriaUsuario.objects.get(id=historia_id)
            historia.notas = nota
            historia.save()
            return JsonResponse({'status': 'success', 'nota': historia.notas})
        except HistoriaUsuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Historia no encontrada'})

    return render(request, 'mainPage/checklist_view.html', {
        'checklists': checklists
    })

@login_required
@require_POST
def toggle_historia_estado(request, historia_id):
    historia = get_object_or_404(HistoriaUsuario, id=historia_id)
    historia.estado = not historia.estado  
    historia.save()
    return JsonResponse({'estado': historia.estado})


@login_required
def add_historias_to_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id, user=request.user)
    historias = HistoriaUsuario.objects.all()  

    if request.method == 'POST':
        historias_ids = request.POST.getlist('historias') 
        historias_seleccionadas = HistoriaUsuario.objects.filter(id__in=historias_ids)

        checklist.historias.add(*historias_seleccionadas) 
        return redirect('checklist_view') 

    return render(request, 'mainPage/add_historias_to_checklist.html', {
        'checklist': checklist,
        'historias': historias,
    })

def checklist_estado(request, checklist_id):
    if request.method == 'POST':
        checklist = get_object_or_404(Checklist, id=checklist_id)
        checklist.estado = not checklist.estado  
        checklist.save()
        return JsonResponse({'estado': checklist.estado})
