from django import forms
from django.core.exceptions import ValidationError
from .models import Carrera

class CarreraForm(forms.ModelForm):
    """
    Formulario para crear y editar carreras
    """
    class Meta:
        model = Carrera
        fields = ['nombre', 'codigo', 'descripcion', 'duracion_anios', 'activa']
        labels = {
            'nombre': 'Nombre de la Carrera',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'duracion_anios': 'Duración en Años',
            'activa': 'Carrera Activa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Técnico en Programación'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej: TP2024', 'style': 'text-transform: uppercase;'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la carrera...'}),
            'duracion_anios': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            # Validar unicidad (excepto si estamos editando la misma carrera)
            if self.instance.pk:
                if Carrera.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una carrera con este nombre.')
            else:
                if Carrera.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError('Ya existe una carrera con este nombre.')
        
        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper().strip()
            # Validar unicidad (excepto si estamos editando la misma carrera)
            if self.instance.pk:
                if Carrera.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una carrera con este código.')
            else:
                if Carrera.objects.filter(codigo__iexact=codigo).exists():
                    raise ValidationError('Ya existe una carrera con este código.')
        
        return codigo

