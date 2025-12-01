"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    # Gestión de Inscripciones
    path('', views.InscripcionListView.as_view(), name='inscripcion_list'),
    path('crear/', views.InscripcionCreateView.as_view(), name='inscripcion_create'),
    path('<int:pk>/dar-baja/', views.InscripcionBajaView.as_view(), name='inscripcion_baja'),
    path('ajax/load-materias/', views.load_materias, name='ajax_load_materias'),
]
