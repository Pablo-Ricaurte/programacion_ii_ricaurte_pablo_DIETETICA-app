from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from consultorio.models import (
    Paciente,
    Nutricionista,
    Alimento,
    PlanNutricional,
    Consulta,
)

@login_required
def home_view(request):
    ultimas_consultas = Consulta.objects.select_related(
        'paciente', 'nutricionista', 'plan_nutricional'
    )[:5]

    context = {
        'total_pacientes': Paciente.objects.count(),
        'total_nutricionistas': Nutricionista.objects.filter(activo=True).count(),
        'total_alimentos': Alimento.objects.count(),
        'total_planes': PlanNutricional.objects.count(),
        'total_consultas': Consulta.objects.count(),
        'ultimas_consultas': ultimas_consultas,
    }
    return render(request, 'consultorio/home.html', context)