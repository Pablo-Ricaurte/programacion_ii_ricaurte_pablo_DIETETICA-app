from django import forms
from consultorio.models.paciente import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombres',
            'apellidos',
            'cedula',
            'fecha_nacimiento',
            'sexo',
            'telefono',
            'email',
            'alergias_observaciones',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. María José',
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Andrade Pérez',
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10 dígitos numéricos',
                'maxlength': '10',
            }),
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 0991234567',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'paciente@correo.com',
            }),
            'alergias_observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alergias alimentarias, intolerancias o antecedentes...',
            }),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula', '').strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError(
                'La cédula debe contener exactamente 10 dígitos numéricos.'
            )
        return cedula