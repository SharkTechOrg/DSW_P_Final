from django.contrib import admin
from .models import Alumno


# Register your models here.
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Alumno.
    """
    list_display = ('legajo', 'get_nombre_completo', 'get_dni', 'carrera', 'activo', 'fecha_ingreso')
    list_filter = ('activo', 'carrera', 'fecha_ingreso')
    search_fields = ('legajo', 'usuario__first_name', 'usuario__last_name', 'usuario__username', 'usuario__email')
    readonly_fields = ('fecha_baja',)
    ordering = ('legajo',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario',)
        }),
        ('Información Académica', {
            'fields': ('legajo', 'carrera', 'fecha_ingreso')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'direccion')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_baja', 'observaciones')
        }),
    )
    
    def get_nombre_completo(self, obj):
        return obj.nombre_completo
    get_nombre_completo.short_description = 'Nombre Completo'
    
    def get_dni(self, obj):
        return obj.dni
    get_dni.short_description = 'DNI'
