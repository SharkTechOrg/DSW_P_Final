"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    path('carreras/', views.CarreraListView.as_view(), name='carrera_list'),
    path('carreras/crear/', views.CarreraCreateView.as_view(), name='carrera_create'),
    path('carreras/<int:pk>/editar/', views.CarreraUpdateView.as_view(), name='carrera_update'),
    path('carreras/<int:pk>/eliminar/', views.CarreraDeleteView.as_view(), name='carrera_delete'),
]
