from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from alumno.models import Alumno
from materia.models import Materia
# Create your models here.
class Inscripcion(models.Model):
    """
    Modelo para gestionar las inscripciones de alumnos a materias.
    Tabla intermedia con información adicional.
    """
    alumno = models.ForeignKey(
        Alumno, 
        on_delete=models.CASCADE, 
        related_name='inscripciones',
        verbose_name='Alumno'
    )
    materia = models.ForeignKey(
        Materia, 
        on_delete=models.CASCADE, 
        related_name='inscripciones',
        verbose_name='Materia'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Inscripción')
    fecha_baja = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Baja')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['alumno', 'materia']  # Un alumno no puede inscribirse dos veces a la misma materia
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        estado = "Activa" if self.activa else "Dada de baja"
        return f"{self.alumno.nombre_completo} - {self.materia.nombre} ({estado})"

    def clean(self):
        """Validaciones personalizadas"""
        # Validar que la materia pertenezca a la carrera del alumno
        if self.alumno and self.materia:
            if self.alumno.carrera != self.materia.carrera:
                raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera')
            
            # Validar cupo disponible
            if self.materia.cupo_disponible <= 0 and self.activa:
                raise ValidationError('No hay cupo disponible en esta materia')

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para manejar la lógica de baja
        """
        if not self.pk:  # Nueva inscripción
            self.fecha_inscripcion = timezone.now()
        super().save(*args, **kwargs)

    def dar_de_baja(self):
        """Método para dar de baja la inscripción"""
        self.activa = False
        self.save()
