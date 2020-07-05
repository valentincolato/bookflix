from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Comentario


# Extendemos del original
class UserCreationFormExtends(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")


    class Meta:
        model = User
        fields = ["username", "password1", "password2",
                  "email", "first_name", "last_name"]



class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        exclude = ('username',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'soyPrincipal')

class ProfileCreateForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(required=False)
    foto =forms.ImageField(required=False)
    nickname =forms.CharField(required=True)

    
    class Meta:
        model = Profile
        fields = [
            "fecha_nacimiento","nickname","foto"
        ]
        exclude = ('user', 'soyPrincipal')

        

class CommentCreateForm(forms.ModelForm):
    texto= forms.CharField(required=True,label='Comentario')

    class Meta:
        model = Comentario
        fields = [
            "texto"
        ]
        exclude = ('perfil','libro','fecha' )