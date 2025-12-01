from django.contrib import admin

from .models import Carrera

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'duracion_anios', 'activa', 'fecha_creacion')
    search_fields = ('nombre', 'codigo')
    list_filter = ('activa',)
    ordering = ('nombre',)

admin.site.register(Carrera, CarreraAdmin)