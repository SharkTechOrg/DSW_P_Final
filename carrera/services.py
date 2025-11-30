from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Carrera

class CarreraService:
    """
    Servicio para gestionar la lógica de negocio de carreras
    """
    
    @staticmethod
    def crear_carrera(nombre, codigo, descripcion, duracion_años):
        """
        Crea una nueva carrera con validaciones
        """
        try:
            with transaction.atomic():
                # Validar unicidad
                if Carrera.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError(f'Ya existe una carrera con el nombre "{nombre}"')
                
                if Carrera.objects.filter(codigo__iexact=codigo).exists():
                    raise ValidationError(f'Ya existe una carrera con el código "{codigo}"')
                
                carrera = Carrera.objects.create(
                    nombre=nombre.strip().title(),
                    codigo=codigo.upper(),
                    descripcion=descripcion,
                    duracion_años=duracion_años
                )
                
                return carrera
                
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def eliminar_carrera(carrera_id):
        """
        Elimina una carrera validando que no tenga relaciones
        """
        try:
            carrera = Carrera.objects.get(id=carrera_id)
            
            # Validar que no tenga materias ni alumnos
            if carrera.materias.exists():
                raise ValidationError('No se puede eliminar una carrera que tiene materias asociadas')
            
            if carrera.alumnos.exists():
                raise ValidationError('No se puede eliminar una carrera que tiene alumnos asociados')
            
            carrera.delete()
            return True
            
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera no existe')

