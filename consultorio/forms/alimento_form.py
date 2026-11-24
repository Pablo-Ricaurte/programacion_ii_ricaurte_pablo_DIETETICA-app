from django import forms
from consultorio.models.alimento import Alimento


class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = [
            'nombre',
            'grupo_alimenticio',
            'porcion_gramos',
            'calorias',
            'proteinas_g',
            'carbohidratos_g',
            'grasas_g',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Pechuga de pollo a la plancha',
            }),
            'grupo_alimenticio': forms.Select(attrs={'class': 'form-control'}),
            'porcion_gramos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
            }),
            'calorias': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
            'proteinas_g': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'carbohidratos_g': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'grasas_g': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
        }

    def clean_calorias(self):
        calorias = self.cleaned_data.get('calorias')
        if calorias is not None and calorias <= 0:
            raise forms.ValidationError(
                'Las calorías por porción deben ser mayores a 0 kcal.'
            )
        return calorias

    def clean_porcion_gramos(self):
        porcion = self.cleaned_data.get('porcion_gramos')
        if porcion is not None and porcion <= 0:
            raise forms.ValidationError(
                'La porción de referencia debe ser mayor a 0 gramos.'
            )
        return porcion