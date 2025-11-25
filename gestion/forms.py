from django import forms
from django.contrib.auth.models import User, Group
from .models import Paciente, Diagnostico, Enfermedad, Sintoma, Signo, PruebaLaboratorio, PruebaPosMortem

# Formulario para PACIENTES
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 'email']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# Formulario para USUARIOS (Médicos y Admins)
class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar Contraseña")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
class EnfermedadForm(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = ['nombre', 'descripcion', 'sintomas', 'signos', 'pruebas_lab', 'pruebas_postmortem']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Widgets de Selección Múltiple (Checkboxes)
            'sintomas': forms.CheckboxSelectMultiple(),
            'signos': forms.CheckboxSelectMultiple(),
            'pruebas_lab': forms.CheckboxSelectMultiple(),
            'pruebas_postmortem': forms.CheckboxSelectMultiple(),
        }

class SignoForm(forms.ModelForm):
    class Meta:
        model = Signo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class SintomaForm(forms.ModelForm):
    class Meta:
        model = Sintoma
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# --- FORMULARIO PRINCIPAL: DIAGNÓSTICO ---
class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['paciente', 'enfermedad_diagnosticada', 'sintomas_presentados', 'pruebas_realizadas', 'notas_adicionales']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'enfermedad_diagnosticada': forms.Select(attrs={'class': 'form-select'}),
            'notas_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Usamos checkboxes para que el médico marque lo que vio
            'sintomas_presentados': forms.CheckboxSelectMultiple(),
            'pruebas_realizadas': forms.CheckboxSelectMultiple(),
        }

# --- FORMULARIOS PARA INFERIR ---
class InferenciaForm(forms.Form):
    # Usamos ModelMultipleChoiceField para que Django maneje los IDs correctamente
    sintomas = forms.ModelMultipleChoiceField(
        queryset=Sintoma.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Seleccione los Síntomas del Paciente"
    )
    signos = forms.ModelMultipleChoiceField(
        queryset=Signo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Seleccione los Signos Observados"
    )

