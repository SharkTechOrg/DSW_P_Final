from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario
from .services import UsuarioService

class LoginForm(AuthenticationForm):
    """
    Formulario personalizado de login usando email en lugar de username
    """
    username = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'required': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'required': True
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Intentar autenticar por email
            try:
                usuario = Usuario.objects.get(email=email)
                if usuario.check_password(password):
                    if not usuario.is_active:
                        raise ValidationError('Esta cuenta está desactivada.')
                    self.user_cache = usuario
                else:
                    raise ValidationError('Email o contraseña incorrectos.')
            except Usuario.DoesNotExist:
                raise ValidationError('Email o contraseña incorrectos.')

        return self.cleaned_data


class CambiarPasswordForm(forms.Form):
    """
    Formulario para cambiar contraseña en el primer login
    """
    password_actual = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'})
    )
    nueva_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
        min_length=8,
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    confirmar_password = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar nueva contraseña'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise ValidationError('La contraseña actual es incorrecta.')
        return password_actual

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if nueva_password and confirmar_password:
            if nueva_password != confirmar_password:
                raise ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def save(self):
        nueva_password = self.cleaned_data['nueva_password']
        return UsuarioService.cambiar_password_primer_login(self.user, nueva_password)


class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear y editar usuarios
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(),
        required=False,
        help_text='Dejar vacío para usar DNI como contraseña inicial'
    )
    
    grupos = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Roles/Grupos'
    )

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        labels = {
            'email': 'Correo Electrónico',
            'username': 'DNI',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'username': forms.TextInput(attrs={'placeholder': '12345678', 'maxlength': '8'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import Group
        self.fields['grupos'].queryset = Group.objects.all()
        if self.instance.pk:
            self.fields['grupos'].initial = self.instance.groups.all()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if not username.isdigit() or len(username) != 8:
                raise ValidationError('El DNI debe tener exactamente 8 dígitos.')
            
            if self.instance.pk:
                if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
            else:
                if Usuario.objects.filter(username=username).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if self.instance.pk:
                if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
            else:
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
        
        return email.lower()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if not password:
            password = self.cleaned_data['username']
        
            usuario.set_password(password)
            usuario.set_password(password)
            usuario.primer_login = True
        
        if commit:
            usuario.save()
            grupos = self.cleaned_data.get('grupos')
            if grupos:
                usuario.groups.set(grupos)
        
        return usuario
