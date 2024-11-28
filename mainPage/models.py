from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import Profile
from django.utils.timezone import now


class RiesgoProyecto(models.Model):
    id = models.AutoField(primary_key=True)
    Titulo = models.CharField('Titulo del riesgo',max_length=70,blank=True,null=True)
    descripcion = models.TextField('Descripción del riesgo',blank=True,null=True)
    gravedad = models.PositiveSmallIntegerField('Nivel de gravedad del riesgo',blank=True,null=True)
    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name="riesgos", blank=True)

    def __str__(self):
        datosFila = "Titulo riesgo: " + self.Titulo
        return datosFila

class Miembro(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('User',on_delete=models.CASCADE,
                                 related_name="miembros", blank=True)
    rol = models.PositiveSmallIntegerField('ROL_USUARIO',blank=True)
    equipo = models.ForeignKey('Equipo',on_delete=models.CASCADE,
                                 related_name="miembros", blank=True)
    def __str__(self):
        datosFila = "Nombre miembro: " + self.usuario.username + " - Nombre proyecto: "
        datosFila += self.equipo.proyecto.nombre
        return datosFila

class Equipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70,blank=True,null=True)

    def __str__(self):
        datosFila = "Nombre equipo: " + self.nombre 
        return datosFila

class HistoriaUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de la hu', max_length=70,blank=False,null=False)
    fechaInicio = models.DateField('Fecha de inicio',blank=False,null=False)
    fechaFin = models.DateField('Fecha de finalización',blank=False,null=False)
    estado = models.BooleanField(default= False,blank=True,null=False)
    descripcion = models.TextField('Descripción de la HU',blank=True,null=True)
    #criterio_aceptacion = las HU tienen una relación OneToMany con Historias de usuario, 
    #ver la def de la clase ↑
    miembroAsignado = models.ManyToManyField(Miembro,related_name="historias",blank=False)

    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name="historias", blank=True)
    #consulta para accedar a las historias pertenecientes a cierto proyecto: 
    #algunProyecto.historias.all()

    def __str__(self):
        datosFila = "Nombre historia: " + self.nombre + " - Fecha inicio: " + str(self.fechaInicio)
        datosFila += " - Fecha fin: " + str(self.fechaFin)
        return datosFila
    
    def ObtenerColor(self):
        if self.estado:
            return '#3CC45E'
        else:
            return 'red'

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre del proyecto', max_length=40,blank=False,null=True)
    fechaInicio = models.DateField('Fecha de inicio',blank=False,null=False)
    fechaFin = models.DateField('Fecha de finalización',blank=False,null=False)
    estado = models.BooleanField(default= False,blank=True,null=False) #Esta completo?
    
    #el proyecto tiene una relación OneToMany con Historias de usuario, ver la def de la clase ↑
    equipo = models.OneToOneField(Equipo,on_delete=models.CASCADE,related_name="proyecto",blank=True)
    gestorProyecto = models.ForeignKey('User',on_delete=models.CASCADE,blank=True,null=True)
    #Recursos
    recursos_tecnologicos = models.TextField('Recursos Tecnológicos', blank=True, null=True)
    recurso_financiero = models.DecimalField('Presupuesto', max_digits=10, decimal_places=2, blank=True, null=True)
    estandares_y_plantillas = models.TextField('Estándares y Plantillas', blank=True, null=True)
    reuniones_y_reportes = models.TextField('Reuniones y Reportes', blank=True, null=True)

    def __str__(self):
        datosFila = "Nombre proyecto: " + self.nombre + " - Fecha inicio: " + str(self.fechaInicio)
        datosFila += " - Fecha fin: " + str(self.fechaFin)
        return datosFila

class User(AbstractUser):
    proyectos = models.ManyToManyField(Proyecto,related_name="usuarios", blank=True)

    # agregue el perfil, permite nombre first name, etc
    perfil = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    # -------------información que no quiero de abstract user:------------------------------------------------
    last_login = None

    def __str__(self):
        datosFila = "Nombre usuario: " + self.username + " - Proyecto: "
        return datosFila

    def ObtenerNombre(self):
        return str(self.first_name + self.last_name);


class Reportes(models.Model):
    id = models.AutoField(primary_key=True)
    CATEGORIAS = [
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=1)
    title = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIAS)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    doc = models.FileField(upload_to='doc/', blank=True, null=True)

    def __str__(self):
        return self.title


class Notif (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=1)
    msg = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.msg}"

    
class Notification(models.Model):
        user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
        message = models.TextField()
        link = models.URLField(blank=True, null=True)
        is_read = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)

