"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    path('materias/', views.MateriaListView.as_view(), name='materia_list'),
    path('materias/crear/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
    path('materias-por-carrera/', views.MateriasPorCarreraView.as_view(), name='materias_por_carrera'),
    path('materias-con-cupo/', views.MateriasConCupoView.as_view(), name='materias_con_cupo'),
]
