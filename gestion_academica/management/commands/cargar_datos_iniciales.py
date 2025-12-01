"""
Comando personalizado para cargar datos iniciales de ejemplo
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction

from alumno.models import Alumno
from carrera.models import Carrera
from inscripcion.models import Inscripcion
from materia.models import Materia
from usuario.models import Usuario


class Command(BaseCommand):
    help = 'Carga datos iniciales de ejemplo en el sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de cargar los nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            with transaction.atomic():
                Inscripcion.objects.all().delete()
                Alumno.objects.all().delete()
                Materia.objects.all().delete()
                Carrera.objects.all().delete()
                Usuario.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando datos iniciales...')
        
        try:
            with transaction.atomic():
                # Obtener grupos (deben existir previamente)
                admin_group = Group.objects.get(name='Administradores')
                alumno_group = Group.objects.get(name='Alumnos')

                # Crear usuarios administradores adicionales
                admin_user, created = Usuario.objects.get_or_create(
                    email='admin@crui.edu.ar',
                    defaults={
                        'username': '12345678',
                        'first_name': 'Administrador',
                        'last_name': 'Sistema',
                        'primer_login': False,
                        'is_staff': True,
                        'is_active': True,
                    }
                )
                if created:
                    admin_user.set_password('admin123')
                    admin_user.save()
                    admin_user.groups.add(admin_group)
                    self.stdout.write(f'✓ Usuario administrador creado: {admin_user.email}')

                # Crear carreras de ejemplo
                carreras_data = [
                    {
                        'nombre': 'Técnico Superior en Programación',
                        'codigo': 'TSP2024',
                        'descripcion': 'Carrera técnica orientada al desarrollo de software',
                        'duracion_anios': 3
                    },
                    {
                        'nombre': 'Técnico Superior en Análisis de Sistemas',
                        'codigo': 'TSAS2024',
                        'descripcion': 'Carrera técnica orientada al análisis y diseño de sistemas',
                        'duracion_anios': 3
                    },
                    {
                        'nombre': 'Técnico Superior en Redes y Comunicaciones',
                        'codigo': 'TSRC2024',
                        'descripcion': 'Carrera técnica orientada a redes de datos y comunicaciones',
                        'duracion_anios': 2
                    }
                ]

                carreras = {}
                for carrera_data in carreras_data:
                    carrera, created = Carrera.objects.get_or_create(
                        codigo=carrera_data['codigo'],
                        defaults=carrera_data
                    )
                    carreras[carrera_data['codigo']] = carrera
                    if created:
                        self.stdout.write(f'✓ Carrera creada: {carrera.nombre}')

                # Crear materias de ejemplo
                materias_data = [
                    # Técnico en Programación - 1er año
                    {
                        'nombre': 'Fundamentos de Programación',
                        'codigo': 'PROG101',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Matemática Aplicada',
                        'codigo': 'MAT101',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Programación Orientada a Objetos',
                        'codigo': 'POO102',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 25
                    },
                    # Técnico en Programación - 2do año
                    {
                        'nombre': 'Bases de Datos',
                        'codigo': 'BD201',
                        'carrera': 'TSP2024',
                        'año': 2,
                        'cuatrimestre': 1,
                        'cupo_maximo': 25
                    },
                    {
                        'nombre': 'Desarrollo Web',
                        'codigo': 'WEB202',
                        'carrera': 'TSP2024',
                        'año': 2,
                        'cuatrimestre': 2,
                        'cupo_maximo': 20
                    },
                    # Análisis de Sistemas
                    {
                        'nombre': 'Análisis y Diseño de Sistemas',
                        'codigo': 'ADS101',
                        'carrera': 'TSAS2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Modelado de Procesos',
                        'codigo': 'MP102',
                        'carrera': 'TSAS2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 25
                    },
                    # Redes y Comunicaciones
                    {
                        'nombre': 'Fundamentos de Redes',
                        'codigo': 'RED101',
                        'carrera': 'TSRC2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 25
                    },
                    {
                        'nombre': 'Configuración de Equipos',
                        'codigo': 'CE102',
                        'carrera': 'TSRC2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 20
                    }
                ]

                materias = {}
                for materia_data in materias_data:
                    carrera = carreras[materia_data['carrera']]
                    materia_data['carrera'] = carrera
                    del materia_data['carrera']  # Quitar el código, ya tenemos el objeto
                    
                    materia, created = Materia.objects.get_or_create(
                        codigo=materia_data['codigo'],
                        carrera=carrera,
                        defaults=materia_data
                    )
                    materias[materia_data['codigo']] = materia
                    if created:
                        self.stdout.write(f'✓ Materia creada: {materia.nombre}')

                # Crear alumnos de ejemplo
                alumnos_data = [
                    {
                        'username': '20123456',
                        'first_name': 'Juan Carlos',
                        'last_name': 'González',
                        'email': 'juan.gonzalez@estudiante.crui.edu.ar',
                        'legajo': '2024001',
                        'carrera': 'TSP2024',
                        'fecha_ingreso': '2024-03-01'
                    },
                    {
                        'username': '20234567',
                        'first_name': 'María Elena',
                        'last_name': 'Rodríguez',
                        'email': 'maria.rodriguez@estudiante.crui.edu.ar',
                        'legajo': '2024002',
                        'carrera': 'TSP2024',
                        'fecha_ingreso': '2024-03-01'
                    },
                    {
                        'username': '20345678',
                        'first_name': 'Carlos Alberto',
                        'last_name': 'Fernández',
                        'email': 'carlos.fernandez@estudiante.crui.edu.ar',
                        'legajo': '2024003',
                        'carrera': 'TSAS2024',
                        'fecha_ingreso': '2024-03-01'
                    },
                    {
                        'username': '20456789',
                        'first_name': 'Ana Sofía',
                        'last_name': 'López',
                        'email': 'ana.lopez@estudiante.crui.edu.ar',
                        'legajo': '2024004',
                        'carrera': 'TSRC2024',
                        'fecha_ingreso': '2024-03-01'
                    }
                ]

                alumnos = {}
                for alumno_data in alumnos_data:
                    carrera_codigo = alumno_data['carrera']
                    carrera = carreras[carrera_codigo]
                    
                    # Crear primero el usuario
                    usuario_data = {
                        'username': alumno_data['username'],
                        'email': alumno_data['email'],
                        'first_name': alumno_data['first_name'],
                        'last_name': alumno_data['last_name'],
                        'is_active': True,
                    }
                    
                    usuario, user_created = Usuario.objects.get_or_create(
                        username=alumno_data['username'],
                        defaults=usuario_data
                    )
                    
                    if user_created:
                        usuario.set_password(alumno_data['username'])  # DNI como contraseña
                        usuario.save()
                        usuario.groups.add(alumno_group)  # Agregar al grupo de alumnos
                    
                    # Ahora crear el alumno usando composición
                    alumno_final_data = {
                        'legajo': alumno_data['legajo'],
                        'carrera': carrera,
                        'usuario': usuario,
                        'fecha_ingreso': alumno_data['fecha_ingreso'],
                    }
                    
                    alumno, created = Alumno.objects.get_or_create(
                        legajo=alumno_data['legajo'],
                        defaults=alumno_final_data
                    )
                    alumnos[alumno_data['username']] = alumno
                    if created:
                        self.stdout.write(f'✓ Alumno creado: {alumno.nombre_completo}')
                print("después del for")
                # Crear algunas inscripciones de ejemplo
                inscripciones_data = [
                    # Juan González (Programación) - 1er año
                    {'alumno': '20123456', 'materia': 'PROG101'},
                    {'alumno': '20123456', 'materia': 'MAT101'},
                    
                    # María Rodríguez (Programación) - 1er año
                    {'alumno': '20234567', 'materia': 'PROG101'},
                    {'alumno': '20234567', 'materia': 'MAT101'},
                    {'alumno': '20234567', 'materia': 'POO102'},
                    
                    # Carlos Fernández (Análisis) - 1er año
                    {'alumno': '20345678', 'materia': 'ADS101'},
                    
                    # Ana López (Redes) - 1er año
                    {'alumno': '20456789', 'materia': 'RED101'},
                ]

                for inscripcion_data in inscripciones_data:
                    alumno = alumnos[inscripcion_data['alumno']]
                    materia = materias[inscripcion_data['materia']]
                    
                    inscripcion, created = Inscripcion.objects.get_or_create(
                        alumno=alumno,
                        materia=materia,
                        defaults={'activa': True}
                    )
                    if created:
                        self.stdout.write(f'✓ Inscripción creada: {alumno.nombre_completo} -> {materia.nombre}')

                self.stdout.write(
                    self.style.SUCCESS('¡Datos iniciales cargados exitosamente!')
                )
                
                # Mostrar resumen
                self.stdout.write('\n--- RESUMEN DE DATOS CARGADOS ---')
                self.stdout.write(f'Carreras: {Carrera.objects.count()}')
                self.stdout.write(f'Materias: {Materia.objects.count()}')
                self.stdout.write(f'Alumnos: {Alumno.objects.count()}')
                self.stdout.write(f'Inscripciones: {Inscripcion.objects.filter(activa=True).count()}')
                self.stdout.write(f'Usuarios: {Usuario.objects.count()}')
                
                self.stdout.write('\n--- USUARIOS DE PRUEBA ---')
                self.stdout.write('Administrador: admin@crui.edu.ar / contraseña: admin123')
                self.stdout.write('Invitado: invitado@ejemplo.com / contraseña: 87654321')
                self.stdout.write('Alumnos: usar email del alumno / contraseña: su DNI')
                self.stdout.write('- juan.gonzalez@estudiante.crui.edu.ar / 20123456')
                self.stdout.write('- maria.rodriguez@estudiante.crui.edu.ar / 20234567')
                self.stdout.write('- carlos.fernandez@estudiante.crui.edu.ar / 20345678')
                self.stdout.write('- ana.lopez@estudiante.crui.edu.ar / 20456789')
                

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {str(e)}')
            )
