# Guion para Video Explicativo - Sistema de Gestión Académica

**Duración estimada:** 10-15 minutos.
**Objetivo:** Demostrar el funcionamiento integral del sistema y el cumplimiento de los requisitos.

---

## 1. Introducción (1 minuto)
*   **Pantalla:** Página de Login (`/login/`).
*   **Acción:** Mostrar la interfaz limpia y profesional.
*   **Narración:**
    *   "Bienvenidos a la presentación del Sistema de Gestión Académica."
    *   "Este sistema web, desarrollado en Python y Django, permite administrar de manera integral carreras, materias, alumnos e inscripciones."
    *   "Cuenta con un sistema de roles diferenciados para Administradores, Alumnos e Invitados."

## 2. Rol Administrador (5-6 minutos)
*   **Acción:** Iniciar sesión con credenciales de Administrador.
*   **Pantalla:** Dashboard Principal.
*   **Narración:** "Al ingresar como Administrador, accedemos al panel de control principal."

### A. Gestión de Carreras
*   **Acción:** Navegar a *Administración > Carreras*.
*   **Demo:**
    1.  Mostrar el listado de carreras existentes.
    2.  **Crear una nueva carrera**: Clic en "Crear", llenar formulario (validar código AA1234), guardar.
    3.  Mostrar mensaje de éxito.

### B. Gestión de Materias
*   **Acción:** Navegar a *Administración > Materias*.
*   **Demo:**
    1.  Mostrar listado con paginación.
    2.  **Filtrar**: Usar el filtro por Carrera para mostrar solo las de la carrera creada.
    3.  **Crear Materia**: Crear una materia para esa carrera (validar cupo y año).
    4.  Destacar la validación de integridad (no se puede borrar si tiene alumnos).

### C. Gestión de Alumnos y Usuarios
*   **Acción:** Navegar a *Administración > Alumnos*.
*   **Demo:**
    1.  **Crear Alumno**: Registrar un nuevo alumno. Explicar que esto crea automáticamente su Usuario de acceso.
    2.  Mostrar el cálculo automático del Legajo.
    3.  Mencionar que la contraseña inicial es su DNI.

### D. Gestión de Inscripciones (Vista Admin)
*   **Acción:** Navegar a *Administración > Inscripciones*.
*   **Demo:** Mostrar que el admin puede ver todas las inscripciones y dar de baja si es necesario.

## 3. Rol Alumno (3-4 minutos)
*   **Acción:** Cerrar sesión de Admin e iniciar como el **Alumno** recién creado.
*   **Pantalla:** Primer Login (Cambio de contraseña).
*   **Narración:** "El sistema obliga a cambiar la contraseña en el primer ingreso por seguridad."
*   **Acción:** Cambiar contraseña y acceder al Dashboard de Alumno.

### A. Inscripción a Materias
*   **Acción:** Ir a *Oferta Académica*.
*   **Demo:**
    1.  Ver las materias disponibles para su carrera.
    2.  **Inscribirse**: Hacer clic en "Inscribirse" en la materia creada anteriormente.
    3.  Verificar que el cupo disminuye.

### B. Mis Materias
*   **Acción:** Ir a *Mis Materias*.
*   **Demo:** Ver la materia en la que se acaba de inscribir.

## 4. Rol Invitado (1-2 minutos)
*   **Acción:** Cerrar sesión.
*   **Pantalla:** Login (sin ingresar).
*   **Acción:** Navegar al menú *Consultas* (público).
*   **Demo:**
    1.  Entrar a *Ver Carreras* o *Ver Materias*.
    2.  Mostrar que puede consultar la oferta académica sin necesidad de usuario y contraseña, pero no puede editar ni inscribirse.

## 5. Conclusión (1 minuto)
*   **Pantalla:** Dashboard o Home.
*   **Narración:**
    *   "En resumen, el sistema cumple con todos los requisitos de CRUD, validaciones de negocio, seguridad y roles."
    *   "La arquitectura modular permite escalar y mantener el código fácilmente."
    *   "Muchas gracias."
