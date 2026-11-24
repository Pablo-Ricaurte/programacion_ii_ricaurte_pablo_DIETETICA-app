from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from consultorio.models.alimento import Alimento


class PlanNutricional(models.Model):
    class ObjetivoPlan(models.TextChoices):
        PERDIDA_PESO = 'PERDIDA_PESO', 'Pérdida de Peso'
        GANANCIA_MUSCULAR = 'GANANCIA_MUSCULAR', 'Ganancia Muscular'
        MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento Saludable'
        CLINICO = 'CLINICO', 'Control Clínico / Patologías'

    nombre = models.CharField(max_length=120, verbose_name='Nombre del plan')
    objetivo = models.CharField(
        max_length=20,
        choices=ObjetivoPlan.choices,
        default=ObjetivoPlan.MANTENIMIENTO,
        verbose_name='Objetivo nutricional',
    )
    calorias_diarias = models.PositiveIntegerField(
        verbose_name='Meta calórica diaria (kcal)',
    )
    indicaciones = models.TextField(verbose_name='Indicaciones y horarios')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de finalización')
    alimentos = models.ManyToManyField(
        Alimento,
        related_name='planes_nutricionales',
        blank=True,
        verbose_name='Alimentos incluidos',
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='planes_creados',
        verbose_name='Creado por',
    )

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Plan Nutricional'
        verbose_name_plural = 'Planes Nutricionales'

    def __str__(self):
        return f'{self.nombre} ({self.get_objetivo_display()} - {self.calorias_diarias} kcal)'

    def get_absolute_url(self):
        return reverse('plan_detail', kwargs={'pk': self.pk})