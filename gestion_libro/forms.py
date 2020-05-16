from django import forms 
from .models import Libro

class ProductForm(forms.ModelForm):
    ISBN        = forms.CharField(label='', widget=forms.NumberInput())
    
    class Meta:
        model = Libro
        fields = [
            "ISBN",
        ]