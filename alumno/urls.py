from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlumnoListView.as_view(), name='alumno_list'),
    path('crear/', views.AlumnoCreateView.as_view(), name='alumno_create'),
    path('<int:pk>/', views.AlumnoDetailView.as_view(), name='alumno_detail'),
    path('<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno_update'),
    path('<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno_delete'),
]
