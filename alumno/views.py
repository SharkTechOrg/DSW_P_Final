from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Alumno
from .forms import AlumnoForm
from .services import AlumnoService
from carrera.models import Carrera


# Create your views here.
class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el usuario sea administrador.
    """
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Administradores').exists()
        )
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('admin:index')


class AlumnoListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """
    Vista para listar todos los alumnos con filtros.
    """
    model = Alumno
    template_name = 'gestion_academica/alumnos/list.html'
    context_object_name = 'alumnos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Alumno.objects.select_related('usuario', 'carrera').all()
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = AlumnoService.buscar_alumnos(search)
        
        # Filtro por carrera
        carrera_id = self.request.GET.get('carrera')
        if carrera_id:
            queryset = queryset.filter(carrera_id=carrera_id)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado == 'activo':
            queryset = queryset.filter(activo=True)
        elif estado == 'inactivo':
            queryset = queryset.filter(activo=False)
        
        return queryset.order_by('legajo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carreras'] = Carrera.objects.filter(activa=True)
        context['search'] = self.request.GET.get('search', '')
        context['carrera_seleccionada'] = self.request.GET.get('carrera', '')
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        
        # Contadores para las tarjetas
        context['total_alumnos_count'] = Alumno.objects.count()
        context['alumnos_activos_count'] = Alumno.objects.filter(activo=True).count()
        
        return context


class AlumnoDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """
    Vista para ver el detalle completo de un alumno.
    """
    model = Alumno
    template_name = 'gestion_academica/alumnos/detail.html'
    context_object_name = 'alumno'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se pueden agregar inscripciones, materias, etc.
        return context


class AlumnoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """
    Vista para crear un nuevo alumno.
    Maneja la creación de Usuario y Alumno en una sola transacción.
    """
    model = Alumno
    form_class = AlumnoForm
    template_name = 'gestion_academica/alumnos/form.html'
    success_url = reverse_lazy('alumno_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Sugerir un legajo automático
        kwargs['initial'] = {
            'legajo': AlumnoService.generar_legajo_automatico()
        }
        return kwargs
    
    def form_valid(self, form):
        try:
            alumno = form.save()
            messages.success(
                self.request, 
                f'Alumno {alumno.nombre_completo} (Legajo: {alumno.legajo}) creado exitosamente.'
            )
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, f'Error al crear el alumno: {str(e)}')
            return self.form_invalid(form)


class AlumnoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """
    Vista para editar un alumno existente.
    """
    model = Alumno
    form_class = AlumnoForm
    template_name = 'gestion_academica/alumnos/form.html'
    success_url = reverse_lazy('alumno_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance_usuario'] = self.object.usuario
        return kwargs
    
    def form_valid(self, form):
        try:
            alumno = form.save()
            messages.success(
                self.request, 
                f'Alumno {alumno.nombre_completo} actualizado exitosamente.'
            )
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar el alumno: {str(e)}')
            return self.form_invalid(form)


class AlumnoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    Vista para dar de baja (desactivar) un alumno.
    """
    model = Alumno
    template_name = 'gestion_academica/alumnos/confirm_delete.html'
    success_url = reverse_lazy('alumno_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verificar si tiene inscripciones activas
        # (esto se puede agregar cuando se implemente el modelo Inscripcion)
        
        # Dar de baja en lugar de eliminar
        AlumnoService.dar_de_baja_alumno(
            self.object,
            motivo=f"Baja realizada por {request.user.get_full_name()}"
        )
        
        messages.warning(
            request, 
            f'Alumno {self.object.nombre_completo} dado de baja exitosamente.'
        )
        
        return redirect(self.success_url)
