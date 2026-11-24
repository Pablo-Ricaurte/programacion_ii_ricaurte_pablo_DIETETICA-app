from django import forms
from consultorio.models.consulta import Consulta


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'paciente',
            'nutricionista',
            'plan_nutricional',
            'fecha_consulta',
            'peso_kg',
            'estatura_cm',
            'costo',
            'estado',
            'diagnostico_notas',
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'nutricionista': forms.Select(attrs={'class': 'form-control'}),
            'plan_nutricional': forms.Select(attrs={'class': 'form-control'}),
            'fecha_consulta': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
            'peso_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej. 68.50',
            }),
            'estatura_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 172',
            }),
            'costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej. 35.00',
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'diagnostico_notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Evaluación nutricional, evolución antropométrica y observaciones...',
            }),
        }

    def clean_peso_kg(self):
        peso = self.cleaned_data.get('peso_kg')
        if peso is not None and (peso <= 0 or peso > 400):
            raise forms.ValidationError(
                'El peso debe estar entre 0.1 kg y 400 kg.'
            )
        return peso

    def clean_estatura_cm(self):
        estatura = self.cleaned_data.get('estatura_cm')
        if estatura is not None and (estatura < 30 or estatura > 250):
            raise forms.ValidationError(
                'La estatura debe estar entre 30 cm y 250 cm.'
            )
        return estatura

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if costo is not None and costo < 0:
            raise forms.ValidationError(
                'El costo de la consulta no puede ser negativo.'
            )
        return costo