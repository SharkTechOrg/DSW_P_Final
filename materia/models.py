from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from carrera.models import Carrera
# Create your models here.
class Materia(models.Model):
    """
    Modelo para las materias académicas
    """
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la Materia')
    codigo = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^[A-Z]{2,4}\d{3,4}$', message='Formato: ABC123')],
        verbose_name='Código'
    )
    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.CASCADE, 
        related_name='materias',
        verbose_name='Carrera'
    )
    año = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='Año'
    )
    cuatrimestre = models.PositiveIntegerField(
        choices=[(1, 'Primer Cuatrimestre'), (2, 'Segundo Cuatrimestre')],
        verbose_name='Cuatrimestre'
    )
    cupo_maximo = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Cupo Máximo'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        unique_together = ['carrera', 'codigo']  # No duplicar códigos por carrera
        ordering = ['carrera', 'año', 'cuatrimestre', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.carrera.nombre} ({self.año}° año)"

    def clean(self):
        """Validaciones personalizadas"""
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        
        # Validar que el año no supere la duración de la carrera
        if self.carrera and self.año > self.carrera.duracion_años:
            raise ValidationError(f'El año {self.año} supera la duración de la carrera ({self.carrera.duracion_años} años)')

    @property
    def cupo_disponible(self):
        """Propiedad que calcula el cupo disponible"""
        inscriptos = self.inscripciones.filter(activa=True).count()
        return self.cupo_maximo - inscriptos

    @property
    def tiene_cupo(self):
        """Propiedad que indica si hay cupo disponible"""
        return self.cupo_disponible > 0

    def delete(self, *args, **kwargs):
        """
        Validación: No permitir eliminar si tiene inscripciones activas
        """
        if self.inscripciones.filter(activa=True).exists():
            raise ValidationError('No se puede eliminar una materia que tiene inscripciones activas')
        super().delete(*args, **kwargs)
