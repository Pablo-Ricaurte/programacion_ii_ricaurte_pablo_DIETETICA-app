from django.urls import path, include

urlpatterns = [
    path('', include('consultorio.urls.home_urls')),
    path('', include('consultorio.urls.paciente_urls')),
    path('', include('consultorio.urls.nutricionista_urls')),
    path('', include('consultorio.urls.alimento_urls')),
    path('', include('consultorio.urls.plan_nutricional_urls')),
    path('', include('consultorio.urls.consulta_urls')),
]