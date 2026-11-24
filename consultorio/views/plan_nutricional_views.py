from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from consultorio.models import PlanNutricional
from consultorio.forms import PlanNutricionalForm


def plan_list(request):
    planes = PlanNutricional.objects.prefetch_related('alimentos').all()
    return render(
        request,
        'consultorio/planes/plan_list.html',
        {'planes': planes},
    )


def plan_detail(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    alimentos = plan.alimentos.all()
    consultas = plan.consultas.select_related('paciente', 'nutricionista').all()
    return render(
        request,
        'consultorio/planes/plan_detail.html',
        {
            'plan': plan,
            'alimentos': alimentos,
            'consultas': consultas,
        },
    )


def plan_create(request):
    if request.method == 'POST':
        form = PlanNutricionalForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            if request.user.is_authenticated:
                plan.creado_por = request.user
            else:
                usuario_respaldo = User.objects.first()
                if not usuario_respaldo:
                    messages.error(
                        request,
                        'Crea primero un usuario administrador para registrar planes.',
                    )
                    return redirect('plan_list')
                plan.creado_por = usuario_respaldo
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


def plan_update(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
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


def plan_delete(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan nutricional eliminado.')
        return redirect('plan_list')

    return render(
        request,
        'consultorio/planes/plan_confirm_delete.html',
        {'plan': plan},
    )