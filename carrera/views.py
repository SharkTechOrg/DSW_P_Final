from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.core.exceptions import ValidationError

from usuario.views import AdminRequiredMixin

from .models import Carrera
from .forms import CarreraForm
from .services import CarreraService

# Create your views here.
class CarreraListView(AdminRequiredMixin, ListView):
    """Lista todas las carreras"""
    model = Carrera
    template_name = 'gestion_academica/carreras/list.html'
    context_object_name = 'carreras'
    paginate_by = 10
    
    def get_queryset(self):
        return Carrera.objects.filter(activa=True).order_by('nombre')


class CarreraCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva carrera"""
    model = Carrera
    form_class = CarreraForm
    template_name = 'gestion_academica/carreras/form.html'
    success_url = reverse_lazy('carrera_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Carrera "{self.object.nombre}" creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class CarreraUpdateView(AdminRequiredMixin, UpdateView):
    """Edita una carrera existente"""
    model = Carrera
    form_class = CarreraForm
    template_name = 'gestion_academica/carreras/form.html'
    success_url = reverse_lazy('carrera_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Carrera "{self.object.nombre}" actualizada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class CarreraDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina una carrera"""
    model = Carrera
    template_name = 'gestion_academica/carreras/confirm_delete.html'
    success_url = reverse_lazy('carrera_list')
    
    def post(self, request, *args, **kwargs):
        try:
            carrera = self.get_object()
            CarreraService.eliminar_carrera(carrera.id)
            messages.success(request, f'Carrera "{carrera.nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e.message), extra_tags='danger')
            return redirect('carrera_list')
