from django.urls import path
from consultorio.views.nutricionista_views import (
    nutricionista_list,
    nutricionista_detail,
    nutricionista_create,
    nutricionista_update,
    nutricionista_delete,
)

urlpatterns = [
    path('nutricionistas/', nutricionista_list, name='nutricionista_list'),
    path('nutricionistas/crear/', nutricionista_create, name='nutricionista_create'),
    path('nutricionistas/<int:pk>/', nutricionista_detail, name='nutricionista_detail'),
    path('nutricionistas/<int:pk>/editar/', nutricionista_update, name='nutricionista_update'),
    path('nutricionistas/<int:pk>/eliminar/', nutricionista_delete, name='nutricionista_delete'),
]