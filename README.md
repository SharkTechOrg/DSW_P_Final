# DSW_P_Final
Sistema web desarrollado en Django para la gestión académica de instituciones educativas.

# Sistema de Gestión Académica

Sistema web desarrollado en Django para la gestión académica de instituciones educativas.

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

### 6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```