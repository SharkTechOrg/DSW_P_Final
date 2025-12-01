from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.core.exceptions import ValidationError

from usuario.views import AdminRequiredMixin

from .models import Carrera, Materia
from .forms import MateriaForm, FiltroMateriaForm
from .services import MateriaService

# Create your views here.
# === GESTIÓN DE MATERIAS (Solo Admin) ===

class MateriaListView(AdminRequiredMixin, ListView):
    """Lista todas las materias con filtros"""
    model = Materia
    template_name = 'gestion_academica/materias/list.html'
    context_object_name = 'materias'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Materia.objects.filter(activa=True).select_related('carrera')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(codigo__icontains=search)
            )
        
        # Filtro por carrera
        carrera_id = self.request.GET.get('carrera')
        if carrera_id:
            queryset = queryset.filter(carrera_id=carrera_id)
        
        return queryset.order_by('carrera__nombre', 'año', 'cuatrimestre', 'nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        context['search'] = self.request.GET.get('search', '')
        
        # Calcular estadísticas
        materias_queryset = self.get_queryset()
        context['materias_activas'] = materias_queryset.filter(activa=True).count()
        context['total_cupo'] = sum(m.cupo_maximo for m in materias_queryset)
        context['cupo_disponible'] = sum(m.cupo_disponible for m in materias_queryset)
        
        return context


class MateriaCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva materia"""
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_academica/materias/form.html'
    success_url = reverse_lazy('materia_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Materia "{self.object.nombre}" creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class MateriaUpdateView(AdminRequiredMixin, UpdateView):
    """Edita una materia existente"""
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_academica/materias/form.html'
    success_url = reverse_lazy('materia_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Materia "{self.object.nombre}" actualizada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class MateriaDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina una materia"""
    model = Materia
    template_name = 'gestion_academica/materias/confirm_delete.html'
    success_url = reverse_lazy('materia_list')
    
    def post(self, request, *args, **kwargs):
        try:
            materia = self.get_object()
            MateriaService.eliminar_materia(materia.id)
            messages.success(request, f'Materia "{materia.nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e.message), extra_tags='danger')
            return redirect('materia_list')

class MateriasPorCarreraView(LoginRequiredMixin, TemplateView):
    """Vista para filtrar materias por carrera"""
    template_name = 'gestion_academica/filtros/materias_por_carrera.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carrera_id = self.request.GET.get('carrera')
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        
        if carrera_id:
            try:
                context['materias'] = MateriaService.obtener_materias_por_carrera(carrera_id)
                context['carrera_seleccionada'] = Carrera.objects.get(id=carrera_id)
            except ValidationError as e:
                messages.error(self.request, str(e))
        
        return context
    
class MateriasConCupoView(TemplateView):
    """Vista para ver materias con cupo disponible (pública)"""
    template_name = 'gestion_academica/publico/materias_con_cupo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materias = MateriaService.obtener_materias_con_cupo()
        
        # Aplicar filtros
        carrera_id = self.request.GET.get('carrera')
        anio = self.request.GET.get('anio')
        cuatrimestre = self.request.GET.get('cuatrimestre')
        
        if carrera_id:
            materias = [m for m in materias if str(m.carrera.id) == carrera_id]
        
        if anio:
            materias = [m for m in materias if str(m.año) == anio]
        
        if cuatrimestre:
            materias = [m for m in materias if str(m.cuatrimestre) == cuatrimestre]
        
        context['materias'] = materias
        context['carreras'] = Carrera.objects.filter(activa=True)
        context['filtro_carrera'] = carrera_id or ''
        context['filtro_anio'] = anio or ''
        context['filtro_cuatrimestre'] = cuatrimestre or ''
        
        # Calcular total de cupos disponibles
        context['total_cupos_disponibles'] = sum(m.cupo_disponible for m in materias)
        
        return context
    
class MateriasPorCarreraView(LoginRequiredMixin, TemplateView):
    """Vista para filtrar materias por carrera"""
    template_name = 'gestion_academica/filtros/materias_por_carrera.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carrera_id = self.request.GET.get('carrera')
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        
        if carrera_id:
            try:
                context['materias'] = MateriaService.obtener_materias_por_carrera(carrera_id)
                context['carrera_seleccionada'] = Carrera.objects.get(id=carrera_id)
            except ValidationError as e:
                messages.error(self.request, str(e))
        
        return context