from django.shortcuts import render,redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
@login_required(login_url="/login")
def home(request):
    #return render(request,os.path.join(BASE_DIR,'templates','test.html'),{"noticias":[]})
    return render(request,'home.html',{"hola":1})


#Para los usuarios no logueados
def welcome(request):
    
    if request.user.is_authenticated:
        return render(request, "gestion_usuario/welcome.html")
    
    return redirect('/login')

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            if user is not None:
                do_login(request,user)
                return redirect('/home')
    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    return render(request, "gestion_usuario/register.html",{'form':form})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            return redirect('/home')
    return render(request, "gestion_usuario/login.html",{'form':form})

def logout(request):
    do_logout(request)
    return redirect('/')