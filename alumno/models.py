from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from usuario.models import Usuario
from carrera.models import Carrera
import re


# Create your models here.
class Alumno(models.Model):
    """
    Modelo para gestionar la información académica de los alumnos.
    Extiende el modelo Usuario con datos específicos del alumno.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='alumno',
        verbose_name='Usuario'
    )
    legajo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Legajo',
        help_text='Identificador único del alumno'
    )
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        related_name='alumnos',
        verbose_name='Carrera',
        null=True,
        blank=True,
        help_text='Requerido para completar el registro del alumno'
    )
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    direccion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Dirección'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    fecha_baja = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Baja'
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['legajo']

    def __str__(self):
        return f"{self.legajo} - {self.nombre_completo}"

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    @property
    def dni(self):
        return self.usuario.username

    @property
    def email(self):
        return self.usuario.email

    def clean(self):
        """
        Validaciones personalizadas del modelo.
        """
        # Validar formato del legajo (LEG-YYYY-NNNN) - REMOVIDO A PEDIDO DEL USUARIO
        # if self.legajo:
        #     patron = r'^LEG-\d{4}-\d{4}$'
        #     if not re.match(patron, self.legajo):
        #         raise ValidationError({
        #             'legajo': 'El legajo debe tener el formato LEG-YYYY-NNNN'
        #         })

        # Validar que la fecha de ingreso no sea futura
        if self.fecha_ingreso and self.fecha_ingreso > timezone.now().date():
            raise ValidationError({
                'fecha_ingreso': 'La fecha de ingreso no puede ser futura'
            })

        # Validar que si está inactivo, tenga fecha de baja
        if not self.activo and not self.fecha_baja:
            raise ValidationError({
                'fecha_baja': 'Debe especificar una fecha de baja para alumnos inactivos'
            })

    def dar_de_baja(self, observacion=""):
        """
        Método para dar de baja al alumno.
        """
        self.activo = False
        self.fecha_baja = timezone.now().date()
        if observacion:
            self.observaciones += f"\n[{timezone.now()}] Baja: {observacion}"
        self.save()

    def reactivar(self, observacion=""):
        """
        Método para reactivar al alumno.
        """
        self.activo = True
        self.fecha_baja = None
        if observacion:
            self.observaciones += f"\n[{timezone.now()}] Reactivación: {observacion}"
        self.save()
