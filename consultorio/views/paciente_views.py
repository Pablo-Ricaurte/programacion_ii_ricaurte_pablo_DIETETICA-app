from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from consultorio.models import Paciente
from consultorio.forms import PacienteForm


def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(
        request,
        'consultorio/pacientes/paciente_list.html',
        {'pacientes': pacientes},
    )


def paciente_detail(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consultas = paciente.consultas.select_related(
        'nutricionista', 'plan_nutricional'
    ).all()
    return render(
        request,
        'consultorio/pacientes/paciente_detail.html',
        {
            'paciente': paciente,
            'consultas': consultas,
        },
    )


def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            if request.user.is_authenticated:
                paciente.creado_por = request.user
            else:
                usuario_respaldo = User.objects.first()
                if not usuario_respaldo:
                    messages.error(
                        request,
                        'Crea primero un usuario administrador para registrar pacientes.',
                    )
                    return redirect('paciente_list')
                paciente.creado_por = usuario_respaldo
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


def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
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


def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado del sistema.')
        return redirect('paciente_list')

    return render(
        request,
        'consultorio/pacientes/paciente_confirm_delete.html',
        {'paciente': paciente},
    )