from django.contrib import admin

from inscripcion.models import Inscripcion

# Register your models here.

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'fecha_inscripcion', 'activa')
    list_filter = ('activa', 'materia__carrera')
    search_fields = ('alumno__nombre_completo', 'materia__nombre')
    ordering = ('-fecha_inscripcion',)

admin.site.register(Inscripcion, InscripcionAdmin)