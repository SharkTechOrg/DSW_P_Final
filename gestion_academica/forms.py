from django import forms
from alumno.models import Alumno
from carrera.models import Carrera
from materia.models import Materia

class FiltroMateriaForm(forms.Form):
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True),
        empty_label="Todas las carreras",
        required=False,
        label="Filtrar por Carrera"
    )


class FiltroAlumnoMateriaForm(forms.Form):
    alumno = forms.ModelChoiceField(
        queryset=Alumno.objects.filter(activo=True),
        empty_label="Seleccionar alumno",
        required=False,
        label="Ver materias del alumno"
    )
    
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.filter(activa=True),
        empty_label="Seleccionar materia",
        required=False,
        label="Ver alumnos de la materia"
    )
