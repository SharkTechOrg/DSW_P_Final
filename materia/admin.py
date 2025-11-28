from django.contrib import admin

from .models import Materia
# Register your models here.
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'carrera', 'año', 'cuatrimestre', 'cupo_maximo', 'activa')
    list_filter = ('carrera', 'año', 'cuatrimestre', 'activa')
    search_fields = ('nombre', 'codigo', 'carrera__nombre')
    ordering = ('carrera', 'año', 'cuatrimestre', 'nombre')

admin.site.register(Materia, MateriaAdmin)