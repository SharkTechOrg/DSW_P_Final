from django.shortcuts import redirect, render
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
        queryset = Inscripcion.objects.filter(activa=True).select_related('alumno', 'materia')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(alumno__nombre__icontains=search) | 
                Q(alumno__apellido__icontains=search) |
                Q(alumno__legajo__icontains=search) |
                Q(materia__nombre__icontains=search) |
                Q(materia__codigo__icontains=search)
            )
            
        return queryset.order_by('-fecha_inscripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        # Stats
        context['total_inscripciones'] = Inscripcion.objects.count()
        context['inscripciones_activas'] = Inscripcion.objects.filter(activa=True).count()
        context['inscripciones_inactivas'] = Inscripcion.objects.filter(activa=False).count()
        # Inscripciones de hoy
        from django.utils import timezone
        context['inscripciones_hoy'] = Inscripcion.objects.filter(fecha_inscripcion__date=timezone.now().date()).count()
        return context


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


def load_materias(request):
    """
    Vista AJAX para cargar materias filtradas por carrera del alumno.
    """
    alumno_id = request.GET.get('alumno')
    materias = []
    
    if alumno_id:
        try:
            from alumno.models import Alumno
            from materia.models import Materia
            
            alumno = Alumno.objects.get(pk=alumno_id)
            materias = Materia.objects.filter(carrera=alumno.carrera, activa=True).order_by('año', 'cuatrimestre', 'nombre')
        except (ValueError, Alumno.DoesNotExist):
            pass
    
    return render(request, 'gestion_academica/inscripciones/materias_options.html', {'materias': materias})
