from django.urls import path
from consultorio.views.paciente_views import (
    paciente_list,
    paciente_detail,
    paciente_create,
    paciente_update,
    paciente_delete,
)

urlpatterns = [
    path('pacientes/', paciente_list, name='paciente_list'),
    path('pacientes/crear/', paciente_create, name='paciente_create'),
    path('pacientes/<int:pk>/', paciente_detail, name='paciente_detail'),
    path('pacientes/<int:pk>/editar/', paciente_update, name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', paciente_delete, name='paciente_delete'),
]