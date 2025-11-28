from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from usuario.models import Usuario
from .models import Alumno
from carreras.models import Carrera


class AlumnoForm(forms.ModelForm):
    """
    Formulario completo para crear y editar alumnos.
    Incluye campos de Usuario y Alumno en un solo formulario.
    """
    # Campos del Usuario
    dni = forms.CharField(
        max_length=8,
        label='DNI',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{8}',
            'maxlength': '8'
        }),
        help_text='8 dígitos sin puntos ni espacios'
    )
    first_name = forms.CharField(
        max_length=150,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido'
        })
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'alumno@example.com'
        })
    )
    password = forms.CharField(
        required=False,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar vacío para usar DNI como contraseña'
        }),
        help_text='Si se deja vacío, se usará el DNI como contraseña inicial'
    )

    class Meta:
        model = Alumno
        fields = ['legajo', 'carrera', 'fecha_ingreso', 'telefono', 'direccion', 'observaciones']
        widgets = {
            'legajo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'LEG-2024-0001',
                'pattern': 'LEG-[0-9]{4}-[0-9]{4}'
            }),
            'carrera': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+54 9 11 1234-5678'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle, número, ciudad'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
        }
        labels = {
            'legajo': 'Legajo',
            'carrera': 'Carrera',
            'fecha_ingreso': 'Fecha de Ingreso',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        self.instance_usuario = kwargs.pop('instance_usuario', None)
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, prellenar campos del usuario
        if self.instance and self.instance.pk:
            self.fields['dni'].initial = self.instance.usuario.username
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Dejar vacío para mantener la contraseña actual'
        
        # Filtrar solo carreras activas
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)

    def clean_dni(self):
        """Validar que el DNI tenga 8 dígitos y sea único."""
        dni = self.cleaned_data.get('dni')
        if dni:
            if not dni.isdigit() or len(dni) != 8:
                raise ValidationError('El DNI debe tener exactamente 8 dígitos numéricos')
            
            # Verificar unicidad (excepto si es el mismo alumno que se está editando)
            exists = Usuario.objects.filter(username=dni)
            if self.instance and self.instance.pk:
                exists = exists.exclude(pk=self.instance.usuario.pk)
            if exists.exists():
                raise ValidationError('Ya existe un usuario con este DNI')
        return dni

    def clean_email(self):
        """Validar que el email sea único."""
        email = self.cleaned_data.get('email')
        if email:
            exists = Usuario.objects.filter(email=email)
            if self.instance and self.instance.pk:
                exists = exists.exclude(pk=self.instance.usuario.pk)
            if exists.exists():
                raise ValidationError('Ya existe un usuario con este email')
        return email

    def clean_legajo(self):
        """Validar que el legajo sea único."""
        legajo = self.cleaned_data.get('legajo')
        if legajo:
            exists = Alumno.objects.filter(legajo=legajo)
            if self.instance and self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError('Ya existe un alumno con este legajo')
        return legajo.upper()

    def save(self, commit=True):
        """
        Guardar tanto el Usuario como el Alumno.
        """
        from django.contrib.auth.models import Group
        from django.db import transaction
        
        alumno = super().save(commit=False)
        
        with transaction.atomic():
            # Crear o actualizar Usuario
            if self.instance and self.instance.pk:
                # Edición: actualizar usuario existente
                usuario = self.instance.usuario
                usuario.username = self.cleaned_data['dni']
                usuario.first_name = self.cleaned_data['first_name']
                usuario.last_name = self.cleaned_data['last_name']
                usuario.email = self.cleaned_data['email']
                
                # Solo actualizar contraseña si se proporcionó una nueva
                if self.cleaned_data.get('password'):
                    usuario.set_password(self.cleaned_data['password'])
                
                usuario.save()
            else:
                # Creación: crear nuevo usuario
                usuario = Usuario.objects.create(
                    username=self.cleaned_data['dni'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    email=self.cleaned_data['email'],
                    is_active=True
                )
                
                # Establecer contraseña
                if self.cleaned_data.get('password'):
                    usuario.set_password(self.cleaned_data['password'])
                else:
                    usuario.set_password(self.cleaned_data['dni'])  # DNI como contraseña por defecto
                
                usuario.save()
                
                # Agregar al grupo Alumnos
                try:
                    grupo_alumnos = Group.objects.get(name='Alumnos')
                    usuario.groups.add(grupo_alumnos)
                except Group.DoesNotExist:
                    pass
                
                alumno.usuario = usuario
            
            if commit:
                alumno.save()
        
        return alumno
