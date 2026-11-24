from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from consultorio.models import Alimento
from consultorio.forms import AlimentoForm


def alimento_list(request):
    alimentos = Alimento.objects.all()
    return render(
        request,
        'consultorio/alimentos/alimento_list.html',
        {'alimentos': alimentos},
    )


def alimento_detail(request, pk):
    alimento = get_object_or_404(Alimento, pk=pk)
    planes = alimento.planes_nutricionales.all()
    return render(
        request,
        'consultorio/alimentos/alimento_detail.html',
        {
            'alimento': alimento,
            'planes': planes,
        },
    )


def alimento_create(request):
    if request.method == 'POST':
        form = AlimentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alimento agregado al catálogo.')
            return redirect('alimento_list')
    else:
        form = AlimentoForm()

    return render(
        request,
        'consultorio/alimentos/alimento_form.html',
        {'form': form, 'accion': 'Agregar'},
    )


def alimento_update(request, pk):
    alimento = get_object_or_404(Alimento, pk=pk)
    if request.method == 'POST':
        form = AlimentoForm(request.POST, instance=alimento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información nutricional actualizada.')
            return redirect('alimento_detail', pk=alimento.pk)
    else:
        form = AlimentoForm(instance=alimento)

    return render(
        request,
        'consultorio/alimentos/alimento_form.html',
        {'form': form, 'alimento': alimento, 'accion': 'Editar'},
    )


def alimento_delete(request, pk):
    alimento = get_object_or_404(Alimento, pk=pk)
    if request.method == 'POST':
        alimento.delete()
        messages.success(request, 'Alimento eliminado del catálogo.')
        return redirect('alimento_list')

    return render(
        request,
        'consultorio/alimentos/alimento_confirm_delete.html',
        {'alimento': alimento},
    )