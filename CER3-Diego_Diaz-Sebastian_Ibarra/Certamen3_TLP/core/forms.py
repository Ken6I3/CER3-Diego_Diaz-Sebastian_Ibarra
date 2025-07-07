from django import forms
from .models import Taller

class ProponerTallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        exclude = ['estado', 'usuario']
