from django.contrib import admin
from .models import Carrera

# Register your models here.
@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Carrera.
    """
    list_display = ('codigo', 'nombre', 'duracion_años', 'activa', 'fecha_creacion')
    list_filter = ('activa', 'duracion_años', 'fecha_creacion')
    search_fields = ('nombre', 'codigo', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Detalles', {
            'fields': ('duracion_años', 'activa', 'fecha_creacion')
        }),
    )
