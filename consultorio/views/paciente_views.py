from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from consultorio.models import Paciente
from consultorio.forms import PacienteForm

def _puede_modificar_paciente(user, paciente):
    if user.is_superuser or user.groups.filter(name='administradores').exists():
        return True
    return paciente.creado_por == user


@login_required
@permission_required('consultorio.view_paciente', raise_exception=True)
def paciente_list(request):
    pacientes = Paciente.objects.select_related('creado_por').all()
    return render(
        request,
        'consultorio/pacientes/paciente_list.html',
        {'pacientes': pacientes},
    )


@login_required
@permission_required('consultorio.view_paciente', raise_exception=True)
def paciente_detail(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consultas = paciente.consultas.select_related(
        'nutricionista', 'plan_nutricional'
    ).all()
    puede_editar = _puede_modificar_paciente(request.user, paciente)
    return render(
        request,
        'consultorio/pacientes/paciente_detail.html',
        {
            'paciente': paciente,
            'consultas': consultas,
            'puede_editar': puede_editar,
        },
    )


@login_required
@permission_required('consultorio.add_paciente', raise_exception=True)
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            messages.success(request, 'Paciente registrado exitosamente.')
            return redirect('paciente_list')
    else:
        form = PacienteForm()

    return render(
        request,
        'consultorio/pacientes/paciente_form.html',
        {'form': form, 'accion': 'Registrar'},
    )


@login_required
@permission_required('consultorio.change_paciente', raise_exception=True)
def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if not _puede_modificar_paciente(request.user, paciente):
        raise PermissionDenied

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del paciente actualizados correctamente.')
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)

    return render(
        request,
        'consultorio/pacientes/paciente_form.html',
        {'form': form, 'paciente': paciente, 'accion': 'Editar'},
    )


@login_required
@permission_required('consultorio.delete_paciente', raise_exception=True)
def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if not _puede_modificar_paciente(request.user, paciente):
        raise PermissionDenied

    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado del sistema.')
        return redirect('paciente_list')

    return render(
        request,
        'consultorio/pacientes/paciente_confirm_delete.html',
        {'paciente': paciente},
    )