from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    username = models.CharField(
        max_length=8, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe tener 8 dígitos')],
        verbose_name='DNI',
        db_column='dni'
    )
    primer_login = models.BooleanField(default=True, verbose_name='Primer Login')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"

    @property
    def rol(self):
        if self.is_superuser:
            return 'administrador'
        if self.groups.filter(name='Administradores').exists():
            return 'administrador'
        elif self.groups.filter(name='Alumnos').exists():
            return 'alumno'
        elif self.groups.filter(name='Docentes').exists():
            return 'docente'
        elif self.groups.filter(name='Preceptores').exists():
            return 'preceptor'
        else:
            return 'sin_rol'

    def get_rol_display(self):
        roles = {
            'administrador': 'Administrador',
            'alumno': 'Alumno',
            'docente': 'Docente',
            'preceptor': 'Preceptor',
            'sin_rol': 'Sin rol',
        }
        return roles.get(self.rol, 'Sin rol')

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            # Contraseña inicial es el DNI
            self.set_password(self.username)
        super().save(*args, **kwargs)

    @classmethod
    def crear_con_grupo(cls, username, first_name, last_name, email, grupo_name, password=None):
        from django.db import transaction
        
        with transaction.atomic():
            usuario = cls.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=True
            )
            
            # Establecer contraseña
            if password:
                usuario.set_password(password)
            else:
                usuario.set_password(username)  # DNI como contraseña por defecto
            usuario.save()
            
            # Agregar al grupo especificado
            try:
                grupo = Group.objects.get(name=grupo_name)
                usuario.groups.add(grupo)
            except Group.DoesNotExist:
                pass  # El grupo se creará con el comando crear_grupos
            
            return usuario
