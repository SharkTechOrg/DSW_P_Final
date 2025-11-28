from django import forms
from .models import Carrera


class CarreraForm(forms.ModelForm):
    """
    Formulario para crear y editar carreras.
    """
    class Meta:
        model = Carrera
        fields = ['nombre', 'codigo', 'descripcion', 'duracion_años']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la carrera'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: TS2024',
                'maxlength': '6'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada de la carrera (opcional)'
            }),
            'duracion_años': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'placeholder': 'Años de duración'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Carrera',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'duracion_años': 'Duración (años)',
        }
        help_texts = {
            'codigo': 'Formato: AA1234 (2 letras mayúsculas + 4 dígitos)',
            'duracion_años': 'Entre 1 y 10 años',
        }

    def clean_codigo(self):
        """
        Validación adicional para el código.
        """
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
        return codigo
