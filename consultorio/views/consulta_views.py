from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from consultorio.models import Consulta
from consultorio.forms import ConsultaForm


def consulta_list(request):
    consultas = Consulta.objects.select_related(
        'paciente', 'nutricionista', 'plan_nutricional', 'creado_por'
    ).all()
    return render(
        request,
        'consultorio/consultas/consulta_list.html',
        {'consultas': consultas},
    )


def consulta_detail(request, pk):
    consulta = get_object_or_404(
        Consulta.objects.select_related(
            'paciente', 'nutricionista', 'plan_nutricional', 'creado_por'
        ),
        pk=pk,
    )
    return render(
        request,
        'consultorio/consultas/consulta_detail.html',
        {'consulta': consulta},
    )


def consulta_create(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            if request.user.is_authenticated:
                consulta.creado_por = request.user
            else:
                usuario_respaldo = User.objects.first()
                if not usuario_respaldo:
                    messages.error(
                        request,
                        'Crea primero un usuario administrador para registrar consultas.',
                    )
                    return redirect('consulta_list')
                consulta.creado_por = usuario_respaldo
            consulta.save()
            messages.success(request, 'Consulta médica registrada exitosamente.')
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    return render(
        request,
        'consultorio/consultas/consulta_form.html',
        {'form': form, 'accion': 'Programar / Registrar'},
    )


def consulta_update(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada correctamente.')
            return redirect('consulta_detail', pk=consulta.pk)
    else:
        form = ConsultaForm(instance=consulta)

    return render(
        request,
        'consultorio/consultas/consulta_form.html',
        {'form': form, 'consulta': consulta, 'accion': 'Editar'},
    )


def consulta_delete(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada del historial.')
        return redirect('consulta_list')

    return render(
        request,
        'consultorio/consultas/consulta_confirm_delete.html',
        {'consulta': consulta},
    )