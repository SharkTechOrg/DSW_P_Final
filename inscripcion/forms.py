from django import forms
from django.core.exceptions import ValidationError
from .models import Materia, Alumno, Inscripcion

class InscripcionForm(forms.ModelForm):
    """
    Formulario para gestionar inscripciones
    """
    class Meta:
        model = Inscripcion
        fields = ['alumno', 'materia', 'observaciones']
        labels = {
            'alumno': 'Alumno',
            'materia': 'Materia',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones (opcional)...'}),
        }

    def __init__(self, *args, **kwargs):
        carrera_id = kwargs.pop('carrera_id', None)
        super().__init__(*args, **kwargs)
        
        if carrera_id:
            # Filtrar alumnos y materias de la misma carrera
            self.fields['alumno'].queryset = Alumno.objects.filter(carrera_id=carrera_id, activo=True)
            self.fields['materia'].queryset = Materia.objects.filter(carrera_id=carrera_id, activa=True)
        else:
            self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
            self.fields['materia'].queryset = Materia.objects.filter(activa=True)

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get('alumno')
        materia = cleaned_data.get('materia')

        if alumno and materia:
            # Validar que la materia pertenezca a la carrera del alumno
            if alumno.carrera != materia.carrera:
                raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera.')
            
            # Validar que no esté ya inscripto
            if Inscripcion.objects.filter(alumno=alumno, materia=materia).exists():
                raise ValidationError('El alumno ya está inscripto en esta materia.')
            
            # Validar cupo disponible
            if not materia.tiene_cupo:
                raise ValidationError('No hay cupo disponible en esta materia.')

        return cleaned_data
