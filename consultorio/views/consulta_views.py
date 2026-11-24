from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from consultorio.models import Consulta
from consultorio.forms import ConsultaForm


def _puede_modificar_consulta(user, consulta):
    if user.is_superuser or user.groups.filter(name='administradores').exists():
        return True
    return consulta.creado_por == user


@login_required
@permission_required('consultorio.view_consulta', raise_exception=True)
def consulta_list(request):
    consultas = Consulta.objects.select_related(
        'paciente', 'nutricionista', 'plan_nutricional', 'creado_por'
    ).all()
    return render(
        request,
        'consultorio/consultas/consulta_list.html',
        {'consultas': consultas},
    )


@login_required
@permission_required('consultorio.view_consulta', raise_exception=True)
def consulta_detail(request, pk):
    consulta = get_object_or_404(
        Consulta.objects.select_related(
            'paciente', 'nutricionista', 'plan_nutricional', 'creado_por'
        ),
        pk=pk,
    )
    puede_editar = _puede_modificar_consulta(request.user, consulta)
    return render(
        request,
        'consultorio/consultas/consulta_detail.html',
        {
            'consulta': consulta,
            'puede_editar': puede_editar,
        },
    )


@login_required
@permission_required('consultorio.add_consulta', raise_exception=True)
def consulta_create(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.creado_por = request.user
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


@login_required
@permission_required('consultorio.change_consulta', raise_exception=True)
def consulta_update(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if not _puede_modificar_consulta(request.user, consulta):
        raise PermissionDenied

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


@login_required
@permission_required('consultorio.delete_consulta', raise_exception=True)
def consulta_delete(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if not _puede_modificar_consulta(request.user, consulta):
        raise PermissionDenied

    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada del historial.')
        return redirect('consulta_list')

    return render(
        request,
        'consultorio/consultas/consulta_confirm_delete.html',
        {'consulta': consulta},
    )