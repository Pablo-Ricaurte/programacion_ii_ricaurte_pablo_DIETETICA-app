from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from consultorio.models import PlanNutricional
from consultorio.forms import PlanNutricionalForm


def _puede_modificar_plan(user, plan):
    if user.is_superuser or user.groups.filter(name='administradores').exists():
        return True
    return plan.creado_por == user


@login_required
@permission_required('consultorio.view_plannutricional', raise_exception=True)
def plan_list(request):
    planes = PlanNutricional.objects.select_related('creado_por').prefetch_related('alimentos').all()
    return render(
        request,
        'consultorio/planes/plan_list.html',
        {'planes': planes},
    )


@login_required
@permission_required('consultorio.view_plannutricional', raise_exception=True)
def plan_detail(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    alimentos = plan.alimentos.all()
    consultas = plan.consultas.select_related('paciente', 'nutricionista').all()
    puede_editar = _puede_modificar_plan(request.user, plan)
    return render(
        request,
        'consultorio/planes/plan_detail.html',
        {
            'plan': plan,
            'alimentos': alimentos,
            'consultas': consultas,
            'puede_editar': puede_editar,
        },
    )


@login_required
@permission_required('consultorio.add_plannutricional', raise_exception=True)
def plan_create(request):
    if request.method == 'POST':
        form = PlanNutricionalForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.creado_por = request.user
            plan.save()
            form.save_m2m()
            messages.success(request, 'Plan nutricional creado exitosamente.')
            return redirect('plan_list')
    else:
        form = PlanNutricionalForm()

    return render(
        request,
        'consultorio/planes/plan_form.html',
        {'form': form, 'accion': 'Crear'},
    )


@login_required
@permission_required('consultorio.change_plannutricional', raise_exception=True)
def plan_update(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    if not _puede_modificar_plan(request.user, plan):
        raise PermissionDenied

    if request.method == 'POST':
        form = PlanNutricionalForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan nutricional actualizado correctamente.')
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = PlanNutricionalForm(instance=plan)

    return render(
        request,
        'consultorio/planes/plan_form.html',
        {'form': form, 'plan': plan, 'accion': 'Editar'},
    )


@login_required
@permission_required('consultorio.delete_plannutricional', raise_exception=True)
def plan_delete(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    if not _puede_modificar_plan(request.user, plan):
        raise PermissionDenied

    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan nutricional eliminado.')
        return redirect('plan_list')

    return render(
        request,
        'consultorio/planes/plan_confirm_delete.html',
        {'plan': plan},
    )