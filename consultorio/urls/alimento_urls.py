from django.urls import path
from consultorio.views.alimento_views import (
    alimento_list,
    alimento_detail,
    alimento_create,
    alimento_update,
    alimento_delete,
)

urlpatterns = [
    path('alimentos/', alimento_list, name='alimento_list'),
    path('alimentos/crear/', alimento_create, name='alimento_create'),
    path('alimentos/<int:pk>/', alimento_detail, name='alimento_detail'),
    path('alimentos/<int:pk>/editar/', alimento_update, name='alimento_update'),
    path('alimentos/<int:pk>/eliminar/', alimento_delete, name='alimento_delete'),
]