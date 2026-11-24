from django.urls import path
from consultorio.views.consulta_views import (
    consulta_list,
    consulta_detail,
    consulta_create,
    consulta_update,
    consulta_delete,
)

urlpatterns = [
    path('consultas/', consulta_list, name='consulta_list'),
    path('consultas/crear/', consulta_create, name='consulta_create'),
    path('consultas/<int:pk>/', consulta_detail, name='consulta_detail'),
    path('consultas/<int:pk>/editar/', consulta_update, name='consulta_update'),
    path('consultas/<int:pk>/eliminar/', consulta_delete, name='consulta_delete'),
]