from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile





# Extendemos del original
class UserCreationFormExtends(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    email = forms.EmailField(label="Correo electrónico")
    first_name= forms.CharField(label="Nombre")
    last_name= forms.CharField(label="Apellido")




    class Meta:
        model = User
        fields = ["username", "password1", "password2","email","first_name","last_name"]





class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name"]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude =('user',  )