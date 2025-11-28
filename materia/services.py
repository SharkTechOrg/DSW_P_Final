from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import  Carrera, Materia


class MateriaService:
    """
    Servicio para gestionar la lógica de negocio de materias
    """
    
    @staticmethod
    def crear_materia(nombre, codigo, carrera_id, año, cuatrimestre, cupo_maximo, descripcion=""):
        """
        Crea una nueva materia con validaciones
        """
        try:
            with transaction.atomic():
                carrera = Carrera.objects.get(id=carrera_id)
                
                # Validar que no exista la combinación carrera-código
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exists():
                    raise ValidationError(f'Ya existe una materia con código "{codigo}" en esta carrera')
                
                # Validar que el año no supere la duración de la carrera
                if año > carrera.duracion_años:
                    raise ValidationError(f'El año {año} supera la duración de la carrera ({carrera.duracion_años} años)')
                
                materia = Materia.objects.create(
                    nombre=nombre.strip().title(),
                    codigo=codigo.upper(),
                    carrera=carrera,
                    año=año,
                    cuatrimestre=cuatrimestre,
                    cupo_maximo=cupo_maximo,
                    descripcion=descripcion
                )
                
                return materia
                
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def eliminar_materia(materia_id):
        """
        Elimina una materia validando que no tenga inscripciones activas
        """
        try:
            materia = Materia.objects.get(id=materia_id)
            
            # Validar que no tenga inscripciones activas
            if materia.inscripciones.filter(activa=True).exists():
                raise ValidationError('No se puede eliminar una materia que tiene inscripciones activas')
            
            materia.delete()
            return True
            
        except Materia.DoesNotExist:
            raise ValidationError('La materia no existe')
    
    @staticmethod
    def obtener_materias_por_carrera(carrera_id):
        """
        Obtiene todas las materias de una carrera específica
        """
        try:
            carrera = Carrera.objects.get(id=carrera_id)
            return Materia.objects.filter(carrera=carrera, activa=True).order_by('año', 'cuatrimestre', 'nombre')
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')
    
    @staticmethod
    def obtener_materias_con_cupo():
        """
        Obtiene todas las materias que tienen cupo disponible
        """
        materias_con_cupo = []
        for materia in Materia.objects.filter(activa=True):
            if materia.tiene_cupo:
                materias_con_cupo.append(materia)
        return materias_con_cupo

