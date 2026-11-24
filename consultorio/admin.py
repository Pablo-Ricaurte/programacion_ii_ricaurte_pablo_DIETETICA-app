from django.contrib import admin
from consultorio.models import (
    Paciente,
    Nutricionista,
    Alimento,
    PlanNutricional,
    Consulta,
)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'apellidos', 'nombres', 'sexo', 'telefono', 'creado_por')
    list_filter = ('sexo', 'fecha_registro')
    search_fields = ('cedula', 'nombres', 'apellidos', 'email')


@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ('registro_profesional', 'apellidos', 'nombres', 'especialidad', 'activo')
    list_filter = ('especialidad', 'activo')
    search_fields = ('registro_profesional', 'nombres', 'apellidos', 'email')


@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo_alimenticio', 'porcion_gramos', 'calorias', 'proteinas_g', 'carbohidratos_g', 'grasas_g')
    list_filter = ('grupo_alimenticio',)
    search_fields = ('nombre',)


@admin.register(PlanNutricional)
class PlanNutricionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'objetivo', 'calorias_diarias', 'fecha_inicio', 'fecha_fin', 'creado_por')
    list_filter = ('objetivo', 'fecha_inicio')
    search_fields = ('nombre', 'indicaciones')
    filter_horizontal = ('alimentos',)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('fecha_consulta', 'paciente', 'nutricionista', 'plan_nutricional', 'peso_kg', 'costo', 'estado', 'creado_por')
    list_filter = ('estado', 'fecha_consulta', 'nutricionista')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'paciente__cedula', 'diagnostico_notas')