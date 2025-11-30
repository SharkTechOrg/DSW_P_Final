from django.shortcuts import redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout

from .models import Usuario
from .forms import CambiarPasswordForm, LoginForm, UsuarioForm

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere grupo de administrador"""
    def test_func(self):
        return (self.request.user.is_authenticated and 
                self.request.user.groups.filter(name='Administradores').exists())
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')


class AlumnoRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere grupo de alumno"""
    def test_func(self):
        return (self.request.user.is_authenticated and 
                self.request.user.groups.filter(name='Alumnos').exists())
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

# === VISTAS DE AUTENTICACIÓN ===

class LoginView(View):
    """Vista para el login del sistema"""
    template_name = 'gestion_academica/auth/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Verificar si es primer login
            if user.primer_login:
                messages.info(request, 'Debes cambiar tu contraseña en el primer acceso.')
                return redirect('cambiar_password_primer_login')
            
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect('dashboard')
        
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Vista para el logout del sistema"""
    def get(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('login')


class CambiarPasswordView(LoginRequiredMixin, View):
    """Vista para cambiar contraseña (uso general)"""
    template_name = 'gestion_academica/auth/cambiar_password.html'
    
    def get(self, request):
        form = CambiarPasswordForm(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('dashboard')
        
        return render(request, self.template_name, {'form': form})


class UsuarioListView(AdminRequiredMixin, ListView):
    """Lista todos los usuarios"""
    model = Usuario
    template_name = 'gestion_academica/usuarios/list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    
    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).order_by('last_name', 'first_name')


class UsuarioCreateView(AdminRequiredMixin, CreateView):
    """Crea un nuevo usuario"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_academica/usuarios/form.html'
    success_url = reverse_lazy('usuario_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Usuario "{self.object.get_full_name()}" creado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    """Edita un usuario existente"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_academica/usuarios/form.html'
    success_url = reverse_lazy('usuario_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Usuario "{self.object.get_full_name()}" actualizado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina un usuario"""
    model = Usuario
    template_name = 'gestion_academica/usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    
    def post(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            nombre = usuario.get_full_name()
            usuario.delete()
            messages.success(request, f'Usuario "{nombre}" eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e.message), extra_tags='danger')
            return redirect('usuario_list')

