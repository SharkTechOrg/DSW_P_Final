from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Crea los grupos y permisos necesarios para el sistema'

    def handle(self, *args, **options):
        self.stdout.write('Creando grupos y permisos...')

        grupos = [
            'Administradores',
            'Alumnos', 
            'Docentes',
            'Preceptores',
            'Invitados'
        ]

        for grupo_name in grupos:
            grupo, created = Group.objects.get_or_create(name=grupo_name)
            if created:
                self.stdout.write(f'✓ Grupo creado: {grupo_name}')

        # Obtener grupos
        admin_group = Group.objects.get(name='Administradores')
        alumno_group = Group.objects.get(name='Alumnos')
        docente_group = Group.objects.get(name='Docentes')
        preceptor_group = Group.objects.get(name='Preceptores')
        invitado_group = Group.objects.get(name='Invitados')

        # Permisos para Administradores (todos los permisos)
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write('✓ Permisos asignados a Administradores: TODOS')

        # Permisos para Alumnos (limitados)
        alumno_permissions = Permission.objects.filter(
            content_type__model__in=['carrera', 'materia'],
            codename__startswith='view_'
        )
        # Agregar permisos para ver sus propias inscripciones
        inscripcion_view = Permission.objects.filter(
            content_type__model='inscripcion',
            codename='view_inscripcion'
        )
        alumno_permissions = list(alumno_permissions) + list(inscripcion_view)
        alumno_group.permissions.set(alumno_permissions)
        self.stdout.write('✓ Permisos asignados a Alumnos: VIEW carreras, materias, inscripciones')

        # Permisos para Docentes (ver y editar materias)
        docente_permissions = Permission.objects.filter(
            content_type__model__in=['carrera', 'materia', 'alumno', 'inscripcion'],
            codename__in=['view_carrera', 'view_materia', 'view_alumno', 'view_inscripcion', 'change_materia']
        )
        docente_group.permissions.set(docente_permissions)
        self.stdout.write('✓ Permisos asignados a Docentes: VIEW/CHANGE materias')

        # Permisos para Preceptores (gestionar alumnos e inscripciones)
        preceptor_permissions = Permission.objects.filter(
            content_type__model__in=['alumno', 'inscripcion', 'carrera', 'materia'],
            codename__in=[
                'view_alumno', 'add_alumno', 'change_alumno',
                'view_inscripcion', 'add_inscripcion', 'change_inscripcion', 'delete_inscripcion',
                'view_carrera', 'view_materia'
            ]
        )
        preceptor_group.permissions.set(preceptor_permissions)
        self.stdout.write('✓ Permisos asignados a Preceptores: CRUD alumnos e inscripciones')

        # Permisos para Invitados (solo lectura limitada)
        invitado_permissions = Permission.objects.filter(
            content_type__model__in=['carrera', 'materia'],
            codename__startswith='view_'
        )
        invitado_group.permissions.set(invitado_permissions)
        self.stdout.write('✓ Permisos asignados a Invitados: VIEW carreras y materias')

        self.stdout.write(
            self.style.SUCCESS('¡Grupos y permisos creados exitosamente!')
        )

        # Mostrar resumen
        self.stdout.write('\n--- GRUPOS CREADOS ---')
        for grupo in Group.objects.all():
            permisos_count = grupo.permissions.count()
            self.stdout.write(f'{grupo.name}: {permisos_count} permisos')
