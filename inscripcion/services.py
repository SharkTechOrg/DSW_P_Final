from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Materia, Alumno, Inscripcion

class InscripcionService:
    """
    Servicio para gestionar la lógica de negocio de inscripciones
    """
    
    @staticmethod
    def inscribir_alumno(alumno_id, materia_id):
        """
        Inscribe un alumno a una materia con todas las validaciones
        """
        try:
            with transaction.atomic():
                alumno = Alumno.objects.get(id=alumno_id)
                materia = Materia.objects.get(id=materia_id)
                
                # Validar que la materia pertenezca a la carrera del alumno
                if alumno.carrera != materia.carrera:
                    raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera')
                
                # Validar si ya existe una inscripción
                inscripcion_existente = Inscripcion.objects.filter(alumno=alumno, materia=materia).first()
                
                if inscripcion_existente:
                    if inscripcion_existente.activa:
                        raise ValidationError('El alumno ya está inscripto en esta materia')
                    else:
                        # Si existe pero está inactiva, reactivarla
                        # Validar cupo disponible antes de reactivar
                        if not materia.tiene_cupo:
                            raise ValidationError('No hay cupo disponible en esta materia')
                            
                        inscripcion_existente.activa = True
                        inscripcion_existente.fecha_baja = None
                        inscripcion_existente.save()
                        return inscripcion_existente
                
                # Validar cupo disponible para nueva inscripción
                if not materia.tiene_cupo:
                    raise ValidationError('No hay cupo disponible en esta materia')
                
                # Crear inscripción nueva
                inscripcion = Inscripcion.objects.create(
                    alumno=alumno,
                    materia=materia,
                    activa=True
                )
                
                return inscripcion
                
        except (Alumno.DoesNotExist, Materia.DoesNotExist):
            raise ValidationError('El alumno o la materia especificados no existen')
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def dar_de_baja_inscripcion(inscripcion_id):
        """
        Da de baja una inscripción
        """
        try:
            inscripcion = Inscripcion.objects.get(id=inscripcion_id, activa=True)
            inscripcion.dar_de_baja()
            return inscripcion
        except Inscripcion.DoesNotExist:
            raise ValidationError('La inscripción no existe o ya está dada de baja')
    
    @staticmethod
    def obtener_inscripciones_alumno(alumno_id):
        """
        Obtiene todas las inscripciones activas de un alumno
        """
        try:
            alumno = Alumno.objects.get(id=alumno_id)
            return Inscripcion.objects.filter(alumno=alumno, activa=True).select_related('materia')
        except Alumno.DoesNotExist:
            raise ValidationError('El alumno especificado no existe')
    
    @staticmethod
    def obtener_alumnos_materia(materia_id):
        """
        Obtiene todos los alumnos inscritos en una materia
        """
        try:
            materia = Materia.objects.get(id=materia_id)
            return Inscripcion.objects.filter(materia=materia, activa=True).select_related('alumno')
        except Materia.DoesNotExist:
            raise ValidationError('La materia especificada no existe')
