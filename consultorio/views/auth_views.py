from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from consultorio.forms import RegistroForm
from consultorio.permissions_setup import configurar_grupos_y_permisos


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            _, grupo_consultores = configurar_grupos_y_permisos()
            usuario.groups.add(grupo_consultores)
            login(request, usuario)
            messages.success(
                request,
                f'¡Bienvenido/a, {usuario.username}! Tu cuenta fue creada con rol de Consultor.',
            )
            return redirect('home')
    else:
        form = RegistroForm()

    return render(
        request,
        'consultorio/auth/registro.html',
        {'form': form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Sesión iniciada como {usuario.username}.')
            siguiente = request.GET.get('next')
            return redirect(siguiente if siguiente else 'home')
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(
        request,
        'consultorio/auth/login.html',
        {'form': form},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')