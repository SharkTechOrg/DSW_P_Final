from django.db import models
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Carrera(models.Model):
    """
    Modelo para las carreras académicas
    """
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre de la Carrera')
    codigo = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(regex=r'^[A-Z]{2,4}\d{2,4}$', message='Formato: AA1234')],
        verbose_name='Código'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    duracion_años = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Duración en Años'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    def clean(self):
        """Validaciones personalizadas"""
        if self.nombre:
            self.nombre = self.nombre.strip().title()

    def delete(self, *args, **kwargs):
        """
        Validación: No permitir eliminar si tiene materias o alumnos
        """
        if self.materias.exists():
            raise ValidationError('No se puede eliminar una carrera que tiene materias asociadas')
        if self.alumnos.exists():
            raise ValidationError('No se puede eliminar una carrera que tiene alumnos asociados')
        super().delete(*args, **kwargs)
