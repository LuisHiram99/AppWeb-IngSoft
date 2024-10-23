from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import Profile


# Create your models here.

class User(AbstractUser):
    nomProyecto = models.TextField('Nombre del proyecto', max_length=40, blank=True, null=True)
    fechaInicio = models.DateField('Fecha de inicio',blank=True, null=True)
    fechaFin = models.DateField('Fecha de finaliación',blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True, null=True)
    #agregue el perfil, permite nombre first name, etc
    perfil = models.OneToOneField(Profile,on_delete=models.CASCADE,blank=True,null=True)
    # -------------información que no quiero de abstract user:------------------------------------------------
    last_login = None


    def __str__(self):
        datosFila = "Nombre usuario: " + self.username + " - Proyecto: "
        return datosFila

    def ObtenerFI(self):
        return self.fechaInicio.isoformat() if self.fechaInicio else None

    def ObtenerFF(self):
        return self.fechaFin.isoformat() if self.fechaFin else None