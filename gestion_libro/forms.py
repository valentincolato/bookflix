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
    #pdf = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Capitulo
        fields = [
            "numero_de_capitulo","pdf"
        ]
        exclude = ['libro']





