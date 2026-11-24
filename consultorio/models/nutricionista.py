from django.db import models
from django.urls import reverse

class Nutricionista(models.Model):
    class Especialidad(models.TextChoices):
        CLINICA = 'CLINICA', 'Nutrición Clínica'
        DEPORTIVA = 'DEPORTIVA', 'Nutrición Deportiva'
        PEDIATRICA = 'PEDIATRICA', 'Nutrición Pediátrica'
        CONTROL_PESO = 'CONTROL_PESO', 'Control de Peso y Metabolismo'
    
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    registro_profesional = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Registro profesional',
    )
    especialidad = models.CharField(
        max_length=20,
        choices=Especialidad.choices,
        default=Especialidad.CLINICA,
        verbose_name='Especialidad',
    )
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    activo = models.BooleanField(default=True, verbose_name='Activo en consultorio')
    
    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Nutricionista'
        verbose_name_plural = 'Nutricionistas'
    
    def __str__(self):
        return f'Lic. {self.nombres} {self.apellidos} ({self.get_especialidad_display()})'
    
    def get_absolute_url(self):
        return reverse('nutricionista_detail', kwargs={'pk': self.pk})