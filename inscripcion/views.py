from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    View, ListView, CreateView
)
from django.core.exceptions import ValidationError

from usuario.views import AdminRequiredMixin, AlumnoRequiredMixin

from .models import Inscripcion
from .forms import InscripcionForm
from .services import InscripcionService
# Create your views here.

# === GESTIÓN DE INSCRIPCIONES ===

class InscripcionListView(AdminRequiredMixin, ListView):
    """Lista todas las inscripciones"""
    model = Inscripcion
    template_name = 'gestion_academica/inscripciones/list.html'
    context_object_name = 'inscripciones'
    paginate_by = 10
    
    def get_queryset(self):
        return Inscripcion.objects.filter(activa=True).select_related('alumno', 'materia').order_by('-fecha_inscripcion')


class InscripcionCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva inscripción"""
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'gestion_academica/inscripciones/form.html'
    success_url = reverse_lazy('inscripcion_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Inscripción creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class InscripcionBajaView(AdminRequiredMixin, AlumnoRequiredMixin, View):
    """Da de baja una inscripción"""
    def post(self, request, pk):
        try:
            inscripcion = InscripcionService.dar_de_baja_inscripcion(pk)
            messages.success(request, f'Inscripción dada de baja exitosamente.')
        except ValidationError as e:
            messages.error(request, str(e.message), extra_tags='danger')
        
        return redirect('inscripcion_list')
