from django.db import models
from django .contrib.auth.models import User
from django.urls import reverse

class Paciente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
    
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    cedula = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        default=Sexo.FEMENINO,
        verbose_name='Sexo',
    )
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    alergias_observaciones = models.TextField(blank=True, verbose_name='Alergias y observaciones clínicas',)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pacientes_creados',
        verbose_name='Registrado por',
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return f'{self.apellidos} {self.nombres} ({self.cedula})'
    
    def get_absolute_url(self):
        return reverse('paciente_detail', kwargs={'pk': self.pk})