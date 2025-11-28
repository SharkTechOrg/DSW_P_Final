from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from .models import Carrera
from .forms import CarreraForm
from .services import CarreraService


# Create your views here.
class CarreraListView(ListView):
    """
    Vista para listar todas las carreras.
    """
    model = Carrera
    template_name = 'carreras/list.html'
    context_object_name = 'carreras'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = CarreraService.buscar_carreras(search)
        return queryset.order_by('nombre')


class CarreraDetailView(DetailView):
    """
    Vista para ver el detalle de una carrera.
    """
    model = Carrera
    template_name = 'carreras/detail.html'
    context_object_name = 'carrera'


class CarreraCreateView(CreateView):
    """
    Vista para crear una nueva carrera.
    """
    model = Carrera
    form_class = CarreraForm
    template_name = 'carreras/form.html'
    success_url = reverse_lazy('carrera_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Carrera "{form.instance.nombre}" creada exitosamente.')
        return super().form_valid(form)


class CarreraUpdateView(UpdateView):
    """
    Vista para editar una carrera existente.
    """
    model = Carrera
    form_class = CarreraForm
    template_name = 'carreras/form.html'
    success_url = reverse_lazy('carrera_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Carrera "{form.instance.nombre}" actualizada exitosamente.')
        return super().form_valid(form)


class CarreraDeleteView(DeleteView):
    """
    Vista para eliminar (desactivar) una carrera.
    """
    model = Carrera
    template_name = 'carreras/confirm_delete.html'
    success_url = reverse_lazy('carrera_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        CarreraService.desactivar_carrera(self.object)
        messages.warning(request, f'Carrera "{self.object.nombre}" desactivada exitosamente.')
        return super().delete(request, *args, **kwargs)
