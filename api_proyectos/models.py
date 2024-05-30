from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Proyectos(models.Model):
    nombre = models.CharField(max_length=250,
                              null=False, blank=False)
    descripcion = models.TextField()
    estado = models.BooleanField(default=False)
    # fecha_fin = models.DateField()


class Tarea(models.Model):
    nombre = models.CharField(max_length=250,
                              null=False, blank=False)
    fecha_ini = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=False)
    proyecto = models.ForeignKey(Proyectos,
                                 on_delete=models.CASCADE,
                                 null=False, blank=False)
