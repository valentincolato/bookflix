from django import forms 
from .models import Libro,Capitulo
from django.contrib import admin
class ProductForm(forms.ModelForm):
    ISBN        = forms.CharField(label='', widget=forms.NumberInput())
    
    class Meta:
        model = Libro
        fields = [
            "ISBN",
        ]
class CapituloForm(forms.ModelForm):

    class Meta:
        model = Capitulo
        exclude = ['libro']





