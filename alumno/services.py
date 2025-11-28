"""
Servicios de lógica de negocio para la app alumno.
"""
from django.db import transaction
from django.utils import timezone
from django.db.models import Q, Count
from .models import Alumno
from usuario.models import Usuario
from carreras.models import Carrera
from django.contrib.auth.models import Group


class AlumnoService:
    """
    Servicio para gestionar la lógica de negocio relacionada con alumnos.
    """
    
    @staticmethod
    def crear_alumno_completo(datos_usuario, datos_alumno):
        """
        Crea un alumno completo con su usuario asociado.
        
        Args:
            datos_usuario: dict con dni, first_name, last_name, email, password (opcional)
            datos_alumno: dict con legajo, carrera, fecha_ingreso, telefono, direccion, observaciones
        
        Returns:
            Alumno: instancia del alumno creado
        """
        with transaction.atomic():
            # Crear usuario
            usuario = Usuario.objects.create(
                username=datos_usuario['dni'],
                first_name=datos_usuario['first_name'],
                last_name=datos_usuario['last_name'],
                email=datos_usuario['email'],
                is_active=True
            )
            
            # Establecer contraseña
            password = datos_usuario.get('password', datos_usuario['dni'])
            usuario.set_password(password)
            usuario.save()
            
            # Agregar al grupo Alumnos
            try:
                grupo_alumnos = Group.objects.get(name='Alumnos')
                usuario.groups.add(grupo_alumnos)
            except Group.DoesNotExist:
                pass
            
            # Crear alumno
            alumno = Alumno.objects.create(
                usuario=usuario,
                legajo=datos_alumno['legajo'],
                carrera=datos_alumno['carrera'],
                fecha_ingreso=datos_alumno['fecha_ingreso'],
                telefono=datos_alumno.get('telefono', ''),
                direccion=datos_alumno.get('direccion', ''),
                observaciones=datos_alumno.get('observaciones', '')
            )
            
            return alumno
    
    @staticmethod
    def obtener_alumnos_activos():
        """
        Obtiene todos los alumnos activos.
        """
        return Alumno.objects.filter(activo=True).select_related('usuario', 'carrera')
    
    @staticmethod
    def obtener_alumnos_por_carrera(carrera_id):
        """
        Obtiene todos los alumnos de una carrera específica.
        """
        return Alumno.objects.filter(
            carrera_id=carrera_id,
            activo=True
        ).select_related('usuario', 'carrera')
    
    @staticmethod
    def obtener_alumno_por_dni(dni):
        """
        Obtiene un alumno por su DNI.
        """
        try:
            usuario = Usuario.objects.get(username=dni)
            return Alumno.objects.get(usuario=usuario)
        except (Usuario.DoesNotExist, Alumno.DoesNotExist):
            return None
    
    @staticmethod
    def obtener_alumno_por_legajo(legajo):
        """
        Obtiene un alumno por su legajo.
        """
        try:
            return Alumno.objects.get(legajo=legajo.upper())
        except Alumno.DoesNotExist:
            return None
    
    @staticmethod
    def generar_legajo_automatico(año=None):
        """
        Genera un legajo automático en formato LEG-YYYY-NNNN.
        
        Args:
            año: año para el legajo (por defecto año actual)
        
        Returns:
            str: legajo generado
        """
        if año is None:
            año = timezone.now().year
        
        # Obtener el último legajo del año
        ultimos_legajos = Alumno.objects.filter(
            legajo__startswith=f'LEG-{año}-'
        ).order_by('-legajo')
        
        if ultimos_legajos.exists():
            ultimo_legajo = ultimos_legajos.first().legajo
            # Extraer el número y sumar 1
            numero = int(ultimo_legajo.split('-')[-1]) + 1
        else:
            numero = 1
        
        return f'LEG-{año}-{numero:04d}'
    
    @staticmethod
    def actualizar_alumno(alumno, datos_usuario=None, datos_alumno=None):
        """
        Actualiza los datos de un alumno y su usuario.
        """
        with transaction.atomic():
            # Actualizar usuario si se proporcionaron datos
            if datos_usuario:
                usuario = alumno.usuario
                for campo, valor in datos_usuario.items():
                    if campo == 'password' and valor:
                        usuario.set_password(valor)
                    elif campo == 'dni':
                        usuario.username = valor
                    else:
                        setattr(usuario, campo, valor)
                usuario.save()
            
            # Actualizar alumno si se proporcionaron datos
            if datos_alumno:
                for campo, valor in datos_alumno.items():
                    setattr(alumno, campo, valor)
                alumno.full_clean()
                alumno.save()
            
            return alumno
    
    @staticmethod
    def dar_de_baja_alumno(alumno, motivo=""):
        """
        Da de baja a un alumno.
        """
        alumno.dar_de_baja(motivo)
        # También desactivar el usuario
        alumno.usuario.is_active = False
        alumno.usuario.save()
        return alumno
    
    @staticmethod
    def reactivar_alumno(alumno, motivo=""):
        """
        Reactiva a un alumno dado de baja.
        """
        alumno.reactivar(motivo)
        # También reactivar el usuario
        alumno.usuario.is_active = True
        alumno.usuario.save()
        return alumno
    
    @staticmethod
    def buscar_alumnos(termino):
        """
        Busca alumnos por nombre, apellido, DNI, legajo o email.
        """
        return Alumno.objects.filter(
            Q(usuario__first_name__icontains=termino) |
            Q(usuario__last_name__icontains=termino) |
            Q(usuario__username__icontains=termino) |
            Q(legajo__icontains=termino) |
            Q(usuario__email__icontains=termino)
        ).select_related('usuario', 'carrera')
    
    @staticmethod
    def obtener_estadisticas_por_carrera():
        """
        Obtiene estadísticas de alumnos por carrera.
        """
        return Carrera.objects.annotate(
            total_alumnos=Count('alumnos', filter=Q(alumnos__activo=True))
        ).filter(activa=True)
    
    @staticmethod
    def validar_disponibilidad_dni(dni, alumno_id=None):
        """
        Valida si un DNI está disponible.
        """
        query = Usuario.objects.filter(username=dni)
        if alumno_id:
            # Excluir el usuario del alumno que se está editando
            try:
                alumno = Alumno.objects.get(pk=alumno_id)
                query = query.exclude(pk=alumno.usuario.pk)
            except Alumno.DoesNotExist:
                pass
        return not query.exists()
    
    @staticmethod
    def validar_disponibilidad_email(email, alumno_id=None):
        """
        Valida si un email está disponible.
        """
        query = Usuario.objects.filter(email=email)
        if alumno_id:
            try:
                alumno = Alumno.objects.get(pk=alumno_id)
                query = query.exclude(pk=alumno.usuario.pk)
            except Alumno.DoesNotExist:
                pass
        return not query.exists()
    
    @staticmethod
    def validar_disponibilidad_legajo(legajo, alumno_id=None):
        """
        Valida si un legajo está disponible.
        """
        query = Alumno.objects.filter(legajo=legajo.upper())
        if alumno_id:
            query = query.exclude(pk=alumno_id)
        return not query.exists()
