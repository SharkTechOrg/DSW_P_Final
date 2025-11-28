from django import forms
from django.core.exceptions import ValidationError
from .models import Carrera, Materia

class MateriaForm(forms.ModelForm):
    """
    Formulario para crear y editar materias
    """
    class Meta:
        model = Materia
        fields = ['nombre', 'codigo', 'carrera', 'año', 'cuatrimestre', 'cupo_maximo', 'descripcion']
        labels = {
            'nombre': 'Nombre de la Materia',
            'codigo': 'Código',
            'carrera': 'Carrera',
            'año': 'Año',
            'cuatrimestre': 'Cuatrimestre',
            'cupo_maximo': 'Cupo Máximo',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Programación I'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej: PROG101', 'style': 'text-transform: uppercase;'}),
            'año': forms.NumberInput(attrs={'min': '1', 'max': '6'}),
            'cupo_maximo': forms.NumberInput(attrs={'min': '1', 'max': '100', 'value': '30'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la materia...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo carreras activas
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)

    def clean(self):
        cleaned_data = super().clean()
        carrera = cleaned_data.get('carrera')
        codigo = cleaned_data.get('codigo')
        año = cleaned_data.get('año')

        # Validar que el código no se repita en la misma carrera
        if carrera and codigo:
            codigo = codigo.upper().strip()
            if self.instance.pk:
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una materia con este código en la carrera seleccionada.')
            else:
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exists():
                    raise ValidationError('Ya existe una materia con este código en la carrera seleccionada.')

        # Validar que el año no supere la duración de la carrera
        if carrera and año:
            if año > carrera.duracion_años:
                raise ValidationError(f'El año {año} supera la duración de la carrera ({carrera.duracion_años} años).')

        return cleaned_data

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper().strip()
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
        return nombre

class FiltroMateriaForm(forms.Form):
    """
    Formulario para filtrar materias por carrera
    """
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True),
        empty_label="Todas las carreras",
        required=False,
        label="Filtrar por Carrera"
    )
