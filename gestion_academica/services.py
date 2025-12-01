"""
Servicios para la lógica de negocio del sistema académico.
Implementa la separación de capas y abstracción de la lógica.
"""


from carrera.models import Carrera
from materia.models import Materia
from alumno.models import Alumno
from usuario.models import Usuario
from inscripcion.models import Inscripcion


class ReportesService:
    """
    Servicio para generar reportes y consultas específicas
    """
    
    @staticmethod
    def reporte_general():
        """
        Genera un reporte general del sistema
        """
        return {
            'total_carreras': Carrera.objects.filter(activa=True).count(),
            'total_materias': Materia.objects.filter(activa=True).count(),
            'total_alumnos': Alumno.objects.filter(activo=True).count(),
            'total_inscripciones': Inscripcion.objects.filter(activa=True).count(),     
            'materias_con_cupo': Materia.objects.filter(activa=True).count(),
            'total_usuarios': Usuario.objects.filter(is_active=True).count(),
        }
    
    @staticmethod
    def materias_con_cupo_por_carrera():
        """
        Retorna materias con cupo agrupadas por carrera
        """
        resultado = {}
        for carrera in Carrera.objects.filter(activa=True):
            materias_con_cupo = []
            for materia in carrera.materias.filter(activa=True):
                if materia.tiene_cupo:
                    materias_con_cupo.append(materia)
            resultado[carrera] = materias_con_cupo
        return resultado
