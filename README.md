# Sistema de Gestión Académica

Sistema web desarrollado en Django para la gestión académica de instituciones educativas.

## Características

- **Gestión de Usuarios**: Sistema de autenticación con roles diferenciados
- **Gestión de Carreras**: CRUD completo para carreras académicas
- **Gestión de Materias**: CRUD completo para materias por carrera
- **Gestión de Alumnos**: CRUD completo para alumnos
- **Sistema de Inscripciones**: Inscripción y baja de alumnos en materias
- **Control de Cupos**: Validación automática de cupos disponibles
- **Filtros y Consultas**: Búsquedas por carrera, materia y alumno
- **Roles de Usuario**: Administrador, Alumno, Invitado

## Tecnologías

- **Python 3.8+**
- **Django 4.x**
- **SQLite** (base de datos por defecto)
- **HTML puro** (sin frameworks CSS)

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/SharkTechOrg/DSW_P_Final.git
cd DSW_P_Final
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. (Opcional) Crear superusuario (administrador principal)
```bash
python manage.py createsuperuser
```

### 6. Cargar Grupos y Permisos Iniciales (Obligatorio)
```bash
python manage.py crear_grupos
```

### 7. Cargar datos de ejemplo (Recomendado)
```bash
python manage.py cargar_datos_iniciales
```

### 8. Ejecutar el servidor
```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Usuarios de Prueba

Después de ejecutar `cargar_datos_iniciales`:

- **Administrador**: admin@crui.edu.ar / admin123
- **Invitado**: invitado@ejemplo.com / 87654321 TODO: quitar grupo invitado, y permitir acceso sin login
- **Alumnos**: usar email del alumno / contraseña: su DNI
   - juan.gonzalez@estudiante.crui.edu.ar / 20123456
   - maria.rodriguez@estudiante.crui.edu.ar / 20234567
   - carlos.fernandez@estudiante.crui.edu.ar / 20345678
   - ana.lopez@estudiante.crui.edu.ar / 20456789