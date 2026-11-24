def roles_usuario(request):
    if not request.user.is_authenticated:
        return {
            'es_admin': False,
            'rol_usuario': 'Invitado',
        }

    es_admin = (
        request.user.is_superuser
        or request.user.groups.filter(name='administradores').exists()
    )

    if request.user.is_superuser:
        rol = 'Superusuario'
    elif es_admin:
        rol = 'Administrador'
    elif request.user.groups.filter(name='consultores').exists():
        rol = 'Consultor'
    else:
        rol = 'Usuario registrado'

    return {
        'es_admin': es_admin,
        'rol_usuario': rol,
    }