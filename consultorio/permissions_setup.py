from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from consultorio.models import (
    Paciente,
    Nutricionista,
    Alimento,
    PlanNutricional,
    Consulta,
)


def configurar_grupos_y_permisos():
    """
    Crea los grupos 'administradores' y 'consultores' y asigna
    los permisos reales de Django para cada modelo de consultorio.
    """
    grupo_admin, _ = Group.objects.get_or_create(name='administradores')
    grupo_consultores, _ = Group.objects.get_or_create(name='consultores')

    modelos = [Paciente, Nutricionista, Alimento, PlanNutricional, Consulta]
    permisos_admin = []

    for modelo in modelos:
        ct = ContentType.objects.get_for_model(modelo)
        permisos_modelo = Permission.objects.filter(content_type=ct)
        permisos_admin.extend(permisos_modelo)

    # Administradores: permisos completos (view, add, change, delete) en las 5 tablas
    grupo_admin.permissions.set(permisos_admin)

    # Consultores: lectura en todo; crear/editar/eliminar en Paciente, Plan y Consulta
    # (la edición y borrado estarán limitados a sus propios registros por regla de propiedad)
    codenames_consultores = [
        'view_paciente', 'add_paciente', 'change_paciente', 'delete_paciente',
        'view_nutricionista',
        'view_alimento',
        'view_plannutricional', 'add_plannutricional', 'change_plannutricional', 'delete_plannutricional',
        'view_consulta', 'add_consulta', 'change_consulta', 'delete_consulta',
    ]
    permisos_consultores = Permission.objects.filter(
        content_type__app_label='consultorio',
        codename__in=codenames_consultores,
    )
    grupo_consultores.permissions.set(permisos_consultores)

    return grupo_admin, grupo_consultores