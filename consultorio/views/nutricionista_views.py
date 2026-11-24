from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from consultorio.models import Nutricionista
from consultorio.forms import NutricionistaForm


def nutricionista_list(request):
    nutricionistas = Nutricionista.objects.all()
    return render(
        request,
        'consultorio/nutricionistas/nutricionista_list.html',
        {'nutricionistas': nutricionistas},
    )


def nutricionista_detail(request, pk):
    nutricionista = get_object_or_404(Nutricionista, pk=pk)
    consultas = nutricionista.consultas.select_related(
        'paciente', 'plan_nutricional'
    ).all()
    return render(
        request,
        'consultorio/nutricionistas/nutricionista_detail.html',
        {
            'nutricionista': nutricionista,
            'consultas': consultas,
        },
    )


def nutricionista_create(request):
    if request.method == 'POST':
        form = NutricionistaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nutricionista registrado exitosamente.')
            return redirect('nutricionista_list')
    else:
        form = NutricionistaForm()

    return render(
        request,
        'consultorio/nutricionistas/nutricionista_form.html',
        {'form': form, 'accion': 'Registrar'},
    )


def nutricionista_update(request, pk):
    nutricionista = get_object_or_404(Nutricionista, pk=pk)
    if request.method == 'POST':
        form = NutricionistaForm(request.POST, instance=nutricionista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del nutricionista actualizados.')
            return redirect('nutricionista_detail', pk=nutricionista.pk)
    else:
        form = NutricionistaForm(instance=nutricionista)

    return render(
        request,
        'consultorio/nutricionistas/nutricionista_form.html',
        {'form': form, 'nutricionista': nutricionista, 'accion': 'Editar'},
    )


def nutricionista_delete(request, pk):
    nutricionista = get_object_or_404(Nutricionista, pk=pk)
    if request.method == 'POST':
        try:
            nutricionista.delete()
            messages.success(request, 'Nutricionista eliminado exitosamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este nutricionista porque tiene consultas registradas. Márcalo como inactivo en su lugar.',
            )
        return redirect('nutricionista_list')

    return render(
        request,
        'consultorio/nutricionistas/nutricionista_confirm_delete.html',
        {'nutricionista': nutricionista},
    )