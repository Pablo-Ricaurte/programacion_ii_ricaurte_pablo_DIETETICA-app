from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from consultorio.models.paciente import Paciente
from consultorio.models.nutricionista import Nutricionista
from consultorio.models.plan_nutricional import PlanNutricional


class Consulta(models.Model):
    class EstadoConsulta(models.TextChoices):
        PROGRAMADA = 'PROGRAMADA', 'Programada'
        REALIZADA = 'REALIZADA', 'Realizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='consultas',
        verbose_name='Paciente',
    )
    nutricionista = models.ForeignKey(
        Nutricionista,
        on_delete=models.PROTECT,
        related_name='consultas',
        verbose_name='Nutricionista',
    )
    plan_nutricional = models.ForeignKey(
        PlanNutricional,
        on_delete=models.SET_NULL,
        related_name='consultas',
        null=True,
        blank=True,
        verbose_name='Plan nutricional asignado',
    )
    fecha_consulta = models.DateField(verbose_name='Fecha de consulta')
    peso_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Peso (kg)',
    )
    estatura_cm = models.PositiveIntegerField(verbose_name='Estatura (cm)')
    costo = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Costo de consulta (USD)',
    )
    estado = models.CharField(
        max_length=15,
        choices=EstadoConsulta.choices,
        default=EstadoConsulta.PROGRAMADA,
        verbose_name='Estado',
    )
    diagnostico_notas = models.TextField(verbose_name='Diagnóstico y notas clínicas')
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='consultas_creadas',
        verbose_name='Registrado por',
    )

    class Meta:
        ordering = ['-fecha_consulta']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    @property
    def imc(self):
        if self.estatura_cm > 0:
            estatura_m = self.estatura_cm / 100
            return round(float(self.peso_kg) / (estatura_m ** 2), 2)
        return 0

    def __str__(self):
        return f'Consulta: {self.paciente.apellidos} {self.paciente.nombres} - {self.fecha_consulta}'

    def get_absolute_url(self):
        return reverse('consulta_detail', kwargs={'pk': self.pk})