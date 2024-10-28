from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import Profile


# Create your models here.

class HistoriaUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de la hu', max_length=70,blank=False,null=False)
    fechaInicio = models.DateField('Fecha de inicio',blank=False,null=False)
    fechaFin = models.DateField('Fecha de finalización',blank=False,null=False)
    estado = models.BooleanField(default= False,blank=True,null=False)
    #criterio_acept
    #descripcion
    miembroAsignado = models.ManyToManyField('User',related_name="historias",blank=False)

    proyecto = models.ForeignKey('Proyecto',on_delete=models.CASCADE,related_name="historias", blank=True)

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
    # rol_miembros = models.SmallIntegerField('Rol de usuario',blank=True,null=True)
    # id_gestorP = models.PositiveSmallIntegerField('id gestor del proyecto',blank=False,null=False)

    gestorProyecto = models.OneToOneField('User',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        datosFila = "Nombre proyecto: " + self.nombre + " - Fecha inicio: " + str(self.fechaInicio)
        datosFila += " - Fecha fin: " + str(self.fechaFin)
        return datosFila

class User(AbstractUser):
    
    proyectos = models.ManyToManyField(Proyecto, blank=True)
    estado = models.BooleanField(default=True, blank=True, null=False)
    rol = models.SmallIntegerField(default=0, blank=True, null=False)
    gestor_proyecto = models.BooleanField(default=False, blank=True, null=False)

    # agregue el perfil, permite nombre first name, etc
    perfil = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    # -------------información que no quiero de abstract user:------------------------------------------------
    last_login = None

    def __str__(self):
        datosFila = "Nombre usuario: " + self.username + " - Proyecto: "
        return datosFila

    def ObtenerNombre(self):
        return str(self.first_name + self.last_name);

    def SoyGestor(self):
        return self.gestor_proyecto

    def HacerGestor(self):
        self.gestor_proyecto = True
        return

class Reportes(models.Model):
    id = models.AutoField(primary_key=True)
    CATEGORIAS = [
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
    ]

    title = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIAS)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title