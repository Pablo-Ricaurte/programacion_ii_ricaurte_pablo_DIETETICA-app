from django import forms
from consultorio.models.nutricionista import Nutricionista


class NutricionistaForm(forms.ModelForm):
    class Meta:
        model = Nutricionista
        fields = [
            'nombres',
            'apellidos',
            'registro_profesional',
            'especialidad',
            'telefono',
            'email',
            'activo',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Carlos Andrés',
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Mena Salgado',
            }),
            'registro_profesional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. MSP-NUT-2026-001',
            }),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 0987654321',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'nutricionista@consultorio.com',
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_registro_profesional(self):
        codigo = self.cleaned_data.get('registro_profesional', '').strip().upper()
        if len(codigo) < 5:
            raise forms.ValidationError(
                'El código de registro profesional debe tener al menos 5 caracteres.'
            )
        return codigo