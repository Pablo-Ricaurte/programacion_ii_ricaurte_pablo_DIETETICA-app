from django.urls import path
from consultorio.views.plan_nutricional_views import (
    plan_list,
    plan_detail,
    plan_create,
    plan_update,
    plan_delete,
)

urlpatterns = [
    path('planes/', plan_list, name='plan_list'),
    path('planes/crear/', plan_create, name='plan_create'),
    path('planes/<int:pk>/', plan_detail, name='plan_detail'),
    path('planes/<int:pk>/editar/', plan_update, name='plan_update'),
    path('planes/<int:pk>/eliminar/', plan_delete, name='plan_delete'),
]