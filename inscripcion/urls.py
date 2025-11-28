"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    # Gestión de Inscripciones
    path('inscripciones/', views.InscripcionListView.as_view(), name='inscripcion_list'),
    path('inscripciones/crear/', views.InscripcionCreateView.as_view(), name='inscripcion_create'),
    path('inscripciones/<int:pk>/dar-baja/', views.InscripcionBajaView.as_view(), name='inscripcion_baja'),
]
