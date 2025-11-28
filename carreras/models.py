from django.db import models
from django.core.exceptions import ValidationError
import re

# Create your models here.
class Carrera(models.Model):
    """
    Modelo para gestionar las carreras académicas de la institución.
    """
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre de la Carrera'
    )
    codigo = models.CharField(
        max_length=6,
        unique=True,
        verbose_name='Código',
        help_text='Formato: AA1234 (2 letras mayúsculas + 4 dígitos)'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    duracion_años = models.PositiveIntegerField(
        verbose_name='Duración en Años',
        help_text='Duración de la carrera entre 1 y 10 años'
    )
    activa = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def clean(self):
        """
        Validaciones personalizadas del modelo.
        """
        # Validar formato del código (AA1234)
        if self.codigo:
            patron = r'^[A-Z]{2}\d{4}$'
            if not re.match(patron, self.codigo):
                raise ValidationError({
                    'codigo': 'El código debe tener el formato AA1234 (2 letras mayúsculas + 4 dígitos)'
                })
        
        # Validar duración en años (entre 1 y 10)
        if self.duracion_años:
            if self.duracion_años < 1 or self.duracion_años > 10:
                raise ValidationError({
                    'duracion_años': 'La duración debe estar entre 1 y 10 años'
                })

    def delete(self, *args, **kwargs):
        """
        Método delete personalizado para desactivar en lugar de eliminar.
        """
        self.activa = False
        self.save()
