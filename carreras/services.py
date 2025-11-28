"""
Servicios de lógica de negocio para la app carreras.
"""
from django.db.models import Count, Q
from .models import Carrera


class CarreraService:
    """
    Servicio para gestionar la lógica de negocio relacionada con carreras.
    """
    
    @staticmethod
    def get_carreras_activas():
        """
        Obtiene todas las carreras activas.
        """
        return Carrera.objects.filter(activa=True)
    
    @staticmethod
    def get_carrera_by_codigo(codigo):
        """
        Obtiene una carrera por su código.
        """
        try:
            return Carrera.objects.get(codigo=codigo.upper())
        except Carrera.DoesNotExist:
            return None
    
    @staticmethod
    def crear_carrera(datos):
        """
        Crea una nueva carrera.
        """
        carrera = Carrera(**datos)
        carrera.full_clean()
        carrera.save()
        return carrera
    
    @staticmethod
    def actualizar_carrera(carrera, datos):
        """
        Actualiza los datos de una carrera existente.
        """
        for campo, valor in datos.items():
            setattr(carrera, campo, valor)
        carrera.full_clean()
        carrera.save()
        return carrera
    
    @staticmethod
    def desactivar_carrera(carrera):
        """
        Desactiva una carrera (soft delete).
        """
        carrera.activa = False
        carrera.save()
        return carrera
    
    @staticmethod
    def activar_carrera(carrera):
        """
        Activa una carrera previamente desactivada.
        """
        carrera.activa = True
        carrera.save()
        return carrera
    
    @staticmethod
    def buscar_carreras(termino):
        """
        Busca carreras por nombre, código o descripción.
        """
        return Carrera.objects.filter(
            Q(nombre__icontains=termino) |
            Q(codigo__icontains=termino) |
            Q(descripcion__icontains=termino)
        )
