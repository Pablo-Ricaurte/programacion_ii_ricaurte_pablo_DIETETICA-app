from django import forms
from consultorio.models.plan_nutricional import PlanNutricional


class PlanNutricionalForm(forms.ModelForm):
    class Meta:
        model = PlanNutricional
        fields = [
            'nombre',
            'objetivo',
            'calorias_diarias',
            'indicaciones',
            'fecha_inicio',
            'fecha_fin',
            'alimentos',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Plan Déficit Calórico Moderado',
            }),
            'objetivo': forms.Select(attrs={'class': 'form-control'}),
            'calorias_diarias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '800',
                'max': '6000',
            }),
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Distribución de comidas, hidratación y recomendaciones...',
            }),
            'fecha_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
            'fecha_fin': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
            'alimentos': forms.CheckboxSelectMultiple(attrs={
                'class': 'checkbox-list',
            }),
        }

    def clean_calorias_diarias(self):
        calorias = self.cleaned_data.get('calorias_diarias')
        if calorias is not None and calorias < 800:
            raise forms.ValidationError(
                'Por seguridad clínica, la meta calórica diaria no puede ser inferior a 800 kcal.'
            )
        return calorias

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error(
                'fecha_fin',
                'La fecha de finalización no puede ser anterior a la fecha de inicio.',
            )
        return cleaned_data