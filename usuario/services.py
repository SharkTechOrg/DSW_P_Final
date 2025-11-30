from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Usuario

class UsuarioService:
    """
    Servicio para gestionar la lógica de negocio de usuarios
    """
    
    @staticmethod
    def crear_usuario(email, dni, nombre, apellido, grupos=None, password=None):
        """
        Crea un nuevo usuario con validaciones de negocio
        """
        try:
            with transaction.atomic():
                # Validar que no exista el DNI o email
                if Usuario.objects.filter(username=dni).exists():
                    raise ValidationError(f'Ya existe un usuario con DNI {dni}')
                
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError(f'Ya existe un usuario con email {email}')
                
                # Crear usuario
                usuario = Usuario.objects.create_user(
                    email=email,
                    username=dni,
                    first_name=nombre,
                    last_name=apellido,
                    password=password or dni  # Contraseña inicial es el DNI
                )
                
                # Asignar grupos si se proporcionan
                if grupos:
                    usuario.groups.set(grupos)
                
                return usuario
                
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def cambiar_password_primer_login(usuario, nueva_password):
        """
        Cambia la contraseña en el primer login
        """
        if not usuario.primer_login:
            raise ValidationError('El usuario ya cambió su contraseña inicial')
        
        usuario.set_password(nueva_password)
        usuario.primer_login = False
        usuario.save()
        return usuario
    
    @staticmethod
    def autenticar_usuario(email, password):
        """
        Autentica un usuario por email y contraseña
        """
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_password(password):
                return usuario
            return None
        except Usuario.DoesNotExist:
            return None
