# NutriVida — Sistema Web de Consulta de Dietética

Aplicación web desarrollada en **Python y Django** para la gestión clínica y administrativa de un consultorio de dietética y nutrición. Permite administrar expedientes de pacientes, equipo de nutricionistas, catálogo nutricional de alimentos, planes dietéticos personalizados (con relación muchos-a-muchos) y consultas médicas, incorporando autenticación, control de acceso basado en grupos y validación de propiedad sobre los registros.

* **Autor:** Pablo Gabriel Ricaurte Guillén
* **Carrera:** Desarrollo de Software — Universidad UTE
* **Asignatura:** Programación II
* **Repositorio:** `https://github.com/Pablo-Ricaurte/programacion_ii_ricaurte_pablo.git`

---

## 1. Funcionalidades Principales

* **Gestión Integral (CRUD con Vistas Basadas en Funciones):** Operaciones completas de listado, vista detallada, creación, edición y eliminación confirmada mediante peticiones `POST` para **Consultas Médicas**, **Pacientes**, **Planes Nutricionales**, **Nutricionistas** y **Alimentos**.
* **Navegación Relacional Bidireccional:**
  * Desde el detalle de un **Paciente** se visualiza su historial completo de consultas, nutricionistas y planes asignados.
  * Desde el detalle de un **Nutricionista** se listan las citas médicas que ha atendido.
  * Desde un **Plan Nutricional** se gestionan y visualizan los alimentos incluidos (`ManyToManyField`) y las consultas donde fue prescrito; desde cada **Alimento** se muestran los planes en los que participa.
* **Cálculo Automático de IMC:** Cada consulta calcula dinámicamente el Índice de Masa Corporal ($\text{IMC} = \text{peso} / \text{estatura}^2$) a partir de las mediciones antropométricas registradas.
* **Validaciones y Seguridad:** Validaciones personalizadas en formularios (`clean_<campo>` y `clean()`), protección CSRF, manejo de errores `404` (`get_object_or_404`) y `403` (`PermissionDenied`), integridad referencial (`ProtectedError`) y notificaciones visuales mediante `django.contrib.messages`.
* **Control de Acceso por Roles y Propiedad:** Diferenciación estricta entre los grupos **`administradores`** y **`consultores`**, ocultando acciones en plantillas según `perms` y restringiendo la edición/eliminación de los consultores exclusivamente a sus propios registros (`creado_por == request.user`).

---

## 2. Arquitectura y Estructura del Proyecto

El proyecto implementa una arquitectura modular desacoplada por paquetes dentro de la aplicación `consultorio`, evitando archivos planos monolíticos y utilizando plantillas con doble carpeta (`consultorio/templates/consultorio/`) junto con una hoja de estilos CSS propia sin dependencias externas:

```text
dietetica-app/
├── config/                                 # Configuración central del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                         # SQLite, idioma es-ec, rutas de login/logout, context processors
│   ├── urls.py                             # Enrutador raíz (/admin/ y delegación a consultorio.urls)
│   └── wsgi.py
├── consultorio/                            # Aplicación principal del dominio
│   ├── migrations/                         # Migraciones versionadas de la base de datos
│   ├── management/
│   │   └── commands/
│   │       └── poblar_datos.py             # Comando reproducible de grupos, usuarios y datos semilla
│   ├── models/                             # Capa de datos modular (1 archivo por entidad)
│   │   ├── __init__.py                     # Re-exportación de los 5 modelos
│   │   ├── paciente.py
│   │   ├── nutricionista.py
│   │   ├── alimento.py
│   │   ├── plan_nutricional.py
│   │   └── consulta.py
│   ├── forms/                              # Formularios ModelForm, widgets y validaciones clean_*
│   │   ├── __init__.py                     # Re-exportación de todos los formularios
│   │   ├── paciente_form.py
│   │   ├── nutricionista_form.py
│   │   ├── alimento_form.py
│   │   ├── plan_nutricional_form.py
│   │   ├── consulta_form.py
│   │   └── registro_form.py                # UserCreationForm extendido con correo electrónico
│   ├── views/                              # Vistas basadas en funciones (FBV)
│   │   ├── __init__.py                     # Re-exportación de todas las funciones de vista
│   │   ├── home_views.py
│   │   ├── auth_views.py                   # Registro, login y logout por POST
│   │   ├── paciente_views.py
│   │   ├── nutricionista_views.py
│   │   ├── alimento_views.py
│   │   ├── plan_nutricional_views.py
│   │   └── consulta_views.py
│   ├── urls/                               # Enrutadores modulares por entidad
│   │   ├── __init__.py                     # Reúne todas las rutas de la aplicación
│   │   ├── home_urls.py
│   │   ├── auth_urls.py
│   │   ├── paciente_urls.py
│   │   ├── nutricionista_urls.py
│   │   ├── alimento_urls.py
│   │   ├── plan_nutricional_urls.py
│   │   └── consulta_urls.py
│   ├── templates/
│   │   ├── 403.html                        # Pantalla personalizada de acceso denegado
│   │   └── consultorio/                    # Doble carpeta obligatoria para plantillas
│   │       ├── base.html                   # Layout maestro, sidebar dinámica y alertas messages
│   │       ├── home.html                   # Dashboard con métricas y últimas consultas
│   │       ├── auth/                       # login.html, registro.html
│   │       ├── pacientes/                  # list, detail, form, confirm_delete
│   │       ├── nutricionistas/             # list, detail, form, confirm_delete
│   │       ├── alimentos/                  # list, detail, form, confirm_delete
│   │       ├── planes/                     # list, detail, form, confirm_delete
│   │       └── consultas/                  # list, detail, form, confirm_delete
│   ├── static/
│   │   └── consultorio/
│   │       └── css/
│   │           └── estilos.css             # Hoja de estilos propia del consultorio
│   ├── admin.py                            # Configuración del panel Django Admin para los 5 modelos
│   ├── apps.py
│   ├── context_processors.py               # Inyección global de rol_usuario y es_admin en plantillas
│   └── permissions_setup.py                # Creación programática de grupos y asignación de Permission
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## 3. Modelo de Datos y Diagrama Entidad-Relación

El sistema cuenta con **5 tablas de negocio** (más la tabla intermedia generada por Django para la relación muchos-a-muchos y la tabla `auth_user`):

```text
+-----------------------+          +---------------------------+
|       auth.User       |          |       Nutricionista       |
+-----------------------+          +---------------------------+
| PK id                 |          | PK id                     |
|    username           |          |    nombres, apellidos     |
|    email              |          |    registro_profesional   |
+-----------------------+          |    especialidad (Choices) |
   |        |        |             |    telefono, email        |
   | 1:N    | 1:N    | 1:N         |    activo                 |
   |        |        |             +---------------------------+
   |        |        |                           | 1
   |        |        |                           | (related_name='consultas')
   |        |        v                           | on_delete=PROTECT
   |        |   +--------------------------------------------+
   |        |   |                  Consulta                  |
   |        |   +--------------------------------------------+
   |        |   | PK id                                      |
   |        |   | FK paciente_id        -------------------->|---+
   |        |   | FK nutricionista_id   (arriba)             |   | N
   |        |   | FK plan_nutricional_id (nullable) ---->|---+   | (related_name='consultas')
   |        |   | FK creado_por_id      (arriba)         |   |   | on_delete=CASCADE
   |        |   |    fecha_consulta                      |   |   v
   |        |   |    peso_kg, estatura_cm                |   |  +-------------------------+
   |        |   |    costo (DecimalField)                |   |  |        Paciente         |
   |        |   |    estado (TextChoices)                |   |  +-------------------------+
   |        |   |    diagnostico_notas                   |   |  | PK id                   |
   |        |   +----------------------------------------+   |  | FK creado_por_id (User) |
   |        |                                                |  |    nombres, apellidos   |
   |        +-----------------------+                        |  |    cedula (unique)      |
   |                                |                        |  |    fecha_nacimiento     |
   | 1:N                            v                        |  |    sexo (TextChoices)   |
   |            +----------------------------------------+   |  |    telefono, email      |
   +----------->|            PlanNutricional             |<--+  |    alergias_observac.   |
                +----------------------------------------+      +-------------------------+
                | PK id                                  |
                | FK creado_por_id (User)                |
                |    nombre                              |
                |    objetivo (TextChoices)              |
                |    calorias_diarias                    |
                |    indicaciones                        |
                |    fecha_inicio, fecha_fin             |
                +----------------------------------------+
                                 | N
                                 | M2M (related_name='planes_nutricionales')
                                 v M
                +----------------------------------------+
                |                Alimento                |
                +----------------------------------------+
                | PK id                                  |
                |    nombre (unique)                     |
                |    grupo_alimenticio (TextChoices)     |
                |    porcion_gramos                      |
                |    calorias, proteinas_g               |
                |    carbohidratos_g, grasas_g           |
                +----------------------------------------+
```

### Descripción de Relaciones
1. **`Paciente` $\rightarrow$ `Consulta` (`ForeignKey`, `on_delete=models.CASCADE`):** Un paciente puede registrar múltiples consultas. Si se elimina el expediente del paciente, sus citas vinculadas se eliminan en cascada.
2. **`Nutricionista` $\rightarrow$ `Consulta` (`ForeignKey`, `on_delete=models.PROTECT`):** Un nutricionista atiende múltiples consultas. `PROTECT` impide eliminar a un especialista con historial clínico activo.
3. **`PlanNutricional` $\rightarrow$ `Consulta` (`ForeignKey`, `null=True, blank=True, on_delete=models.SET_NULL`):** Una consulta puede asignar un plan nutricional opcional; si el plan se elimina posteriormente, la consulta conserva su historial médico.
4. **`PlanNutricional` $\leftrightarrow$ `Alimento` (`ManyToManyField`, `related_name='planes_nutricionales'`):** Permite asociar múltiples alimentos a cada plan nutricional y consultar desde cada alimento en qué dietas participa.
5. **`User` $\rightarrow$ `Consulta` / `Paciente` / `PlanNutricional` (`ForeignKey`, `on_delete=models.PROTECT`):** Almacena la autoría (`creado_por`) de cada registro para auditar y aplicar la regla de propiedad.

---

## 4. Instalación y Ejecución Local

### Requisitos Previos
* Python 3.10 o superior
* Git

### Pasos para Levantar el Proyecto desde Cero

1. **Clonar el repositorio y ubicarse en la carpeta del proyecto:**
   ```bash
   git clone [https://github.com/Pablo-Ricaurte/programacion_ii_ricaurte_pablo.git](https://github.com/Pablo-Ricaurte/programacion_ii_ricaurte_pablo.git)
   cd programacion_ii_ricaurte_pablo/dietetica-app
   ```

2. **Crear y activar el entorno virtual:**
   * **Linux / macOS (Bash / Zsh):**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Linux (Fish shell):**
     ```fish
     python3 -m venv venv
     source venv/bin/activate.fish
     ```
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar las migraciones de la base de datos SQLite:**
   ```bash
   python manage.py migrate
   ```

5. **Cargar grupos, permisos, usuarios de prueba y datos semilla:**
   ```bash
   python manage.py poblar_datos
   ```
   *(Este comando crea automáticamente los grupos `administradores` y `consultores`, asigna sus permisos reales sobre los 5 modelos, crea 4 usuarios de prueba y pobla al menos 5 registros por cada tabla).*

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   * **Aplicación web:** `http://127.0.0.1:8000/`
   * **Panel de administración Django:** `http://127.0.0.1:8000/admin/`

---

## 5. Usuarios de Prueba, Grupos y Control de Acceso

### Credenciales Precargadas (`python manage.py poblar_datos`)

| Usuario | Contraseña | Rol / Grupo | Capacidades y Permisos |
| :--- | :--- | :--- | :--- |
| `admin_ute` | `AdminUte2026*` | **Superusuario** | Acceso irrestricto a toda la aplicación y al panel `/admin/`. |
| `laura_admin` | `NutriAdmin2026*` | **`administradores`** | Permisos CRUD completos (`view`, `add`, `change`, `delete`) sobre las 5 tablas, sin restricción de autoría. |
| `carlos_consultor` | `Consultor2026*` | **`consultores`** | Lectura de las 5 entidades; creación de consultas, pacientes y planes; edición y borrado **solo de sus propios registros**. |
| `ana_consultora` | `Consultor2026*` | **`consultores`** | Segundo consultor de prueba para verificar el bloqueo (`403 Forbidden`) sobre registros creados por `carlos_consultor` o `laura_admin`. |

*(Nota: Todo usuario nuevo que se registre desde `/registro/` recibe automáticamente el grupo `consultores`).*

### Regla de Propiedad (`creado_por == request.user`)
* Los usuarios pertenecientes al grupo **`consultores`** pueden consultar todos los registros del consultorio y crear nuevos pacientes, planes y consultas.
* Tanto en los listados como en las vistas de detalle, los botones **Editar** y **Eliminar** se ocultan dinámicamente si el registro pertenece a otro usuario.
* Si un consultor intenta acceder directamente mediante URL a `/consultas/<id>/editar/` o `/consultas/<id>/eliminar/` de un registro ajeno, la vista intercepta la petición y responde con **HTTP 403 Forbidden** (`403.html`).

---

## 6. Mapa de Rutas Principales

| Módulo | Ruta Base | Operaciones Disponibles |
| :--- | :--- | :--- |
| **Inicio** | `/` | Dashboard con estadísticas generales y últimas consultas |
| **Autenticación** | `/login/`, `/registro/`, `/logout/` | Inicio de sesión, registro con email y cierre de sesión por `POST` |
| **Consultas** | `/consultas/` | `crear/`, `<int:pk>/`, `<int:pk>/editar/`, `<int:pk>/eliminar/` |
| **Pacientes** | `/pacientes/` | `crear/`, `<int:pk>/`, `<int:pk>/editar/`, `<int:pk>/eliminar/` |
| **Nutricionistas** | `/nutricionistas/` | `crear/`, `<int:pk>/`, `<int:pk>/editar/`, `<int:pk>/eliminar/` |
| **Planes** | `/planes/` | `crear/`, `<int:pk>/`, `<int:pk>/editar/`, `<int:pk>/eliminar/` |
| **Alimentos** | `/alimentos/` | `crear/`, `<int:pk>/`, `<int:pk>/editar/`, `<int:pk>/eliminar/` |
| **Administración** | `/admin/` | Panel administrativo de Django con filtros y búsqueda por entidad |

---

## 7. Estándares de Desarrollo y Control de Versiones

El desarrollo del repositorio se gestionó mediante ramas de trabajo y commits atómicos siguiendo los estándares de nomenclatura (`TIPO-CONSULTORIO-XX-DESCRIPCION` y `tipo(CONSULTORIO-XX): descripción`):

* `CONSULTORIO-01`: Configuración inicial del proyecto Django (`config`), app (`consultorio`) y estructura modular.
* `CONSULTORIO-02`: Implementación de los 5 modelos relacionales (`models/`) y migraciones iniciales.
* `CONSULTORIO-03`: Creación de `ModelForm`, widgets personalizados, validaciones `clean_*` y `RegistroForm`.
* `CONSULTORIO-04`: Desarrollo de vistas basadas en funciones (`views/`) y enrutamiento modular (`urls/`).
* `CONSULTORIO-05`: Diseño de plantillas HTML con doble carpeta (`templates/consultorio/`) y navegación bidireccional.
* `CONSULTORIO-06`: Hoja de estilos CSS propia (`static/consultorio/css/estilos.css`).
* `CONSULTORIO-07`: Sistema de autenticación, grupos (`administradores`, `consultores`), permisos y regla de propiedad.
* `CONSULTORIO-08`: Configuración de `admin.py` y comando reproducible `poblar_datos.py`.
* `CONSULTORIO-09`: Documentación técnica completa en `README.md`.