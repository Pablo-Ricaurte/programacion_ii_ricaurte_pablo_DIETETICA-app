from django.db import models
from django.urls import reverse

class Alimento(models.Model):
    class GrupoAlimenticio(models.TextChoices):
        PROTEINAS = 'PROTEINAS', 'Proteínas'
        CARBOHIDRATOS = 'CARBOHIDRATOS', 'Carbohidratos'
        GRASAS = 'GRASAS', 'Grasas Saludables'
        FRUTAS_VERDURAS = 'FRUTAS_VERDURAS', 'Frutas y Verduras'
        LACTEOS = 'LACTEOS', 'Lácteos y Derivados'
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del alimento',
    )
    grupo_alimenticio = models.CharField(
        max_length=20,
        choices=GrupoAlimenticio.choices,
        default=GrupoAlimenticio.PROTEINAS,
        verbose_name='Grupo alimenticio',
    )
    porcion_gramos = models.PositiveIntegerField(
        default=100,
        verbose_name='Porción de referencia (g)',
    )
    calorias = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Calorías (kcal)',
    )
    proteinas_g = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Proteínas (g)',
    )
    carbohidratos_g = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Carbohidratos (g)',
    )
    grasas_g = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Grasas (g)',
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Alimento'
        verbose_name_plural = 'Alimentos'

    def __str__(self):
        return f'{self.nombre} ({self.calorias} kcal / {self.porcion_gramos}g)'

    def get_absolute_url(self):
        return reverse('alimento_detail', kwargs={'pk': self.pk})