"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.MateriaListView.as_view(), name='materia_list'),
    path('crear/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
    path('por-carrera/', views.MateriasPorCarreraView.as_view(), name='materias_por_carrera'),
    path('con-cupo/', views.MateriasConCupoView.as_view(), name='materias_con_cupo'),
]
