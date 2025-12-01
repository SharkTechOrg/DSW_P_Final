"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Autenticación especial
    path('cambiar-password-primer-login/', views.CambiarPasswordPrimerLoginView.as_view(), name='cambiar_password_primer_login'),
    
    # Vistas específicas para alumnos
    path('mis-materias/', views.MisMateriaView.as_view(), name='mis_materias'),
    path('oferta-academica/', views.OfertaAcademicaView.as_view(), name='oferta_academica'),
    path('inscribirse/<int:materia_id>/', views.InscribirseView.as_view(), name='inscribirse'),
    
    # Vistas para invitados
    path('carreras-publicas/', views.CarrerasPublicasView.as_view(), name='carreras_publicas'),
    path('materias-publicas/', views.MateriasPublicasView.as_view(), name='materias_publicas'),
    
    # Filtros y consultas
    path('materias-por-carrera/', views.MateriasPorCarreraView.as_view(), name='materias_por_carrera'),
    path('alumnos-por-materia/', views.AlumnosPorMateriaView.as_view(), name='alumnos_por_materia'),
    path('materias-con-cupo/', views.MateriasConCupoView.as_view(), name='materias_con_cupo'),
    
    # Reportes
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
]
