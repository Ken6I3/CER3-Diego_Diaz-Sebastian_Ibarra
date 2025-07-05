from django import forms
from .models import Taller

class ProponerTallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        # Incluye todos los campos que el usuario puede llenar, excepto 'estado'
        exclude = ['estado', 'usuario']  # si tienes campo usuario para registrar quien propone
