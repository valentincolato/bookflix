from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserCreationFormExtends, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import get_object_or_404
import os
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from gestion_noticia.views import noticias, ultimas_noticias

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
# @login_required(login_url="/login")


def home(request):
    if request.user.is_authenticated:
        return redirect('home/')

    context = {"estoy_en_home": True, "noticias": ultimas_noticias(3)}    
    return render(request, "home.html", context)


# Para los usuarios no logueados
def welcome(request):
    if request.user.is_authenticated:
        return render(request, "gestion_usuario/welcome.html")
    return redirect('/login')


def register(request):
    form = UserCreationFormExtends()

    if request.method == "POST":
        form = UserCreationFormExtends(data=request.POST)
        if form.is_valid():
            user = form.save()
            prf = Profile(user=user, nickname=user.username)
            prf.save()
            if user is not None:
                do_login(request, user)
                return redirect('/')
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    return render(request, "gestion_usuario/register.html", {'form': form})


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
            # set de sesion
            create_session(request)
            # que pasa si hace login desde /admin????
            return redirect('/')
    return render(request, "gestion_usuario/login.html", {'form': form})


def create_session(request):
    perfil_primario = Profile.objects.get(user=request.user, soyPrincipal=True)
    request.session['perfil'] = perfil_primario.id
    request.session['usuario'] = perfil_primario.user.id


def change_session_profile(request,id):
    request.session['perfil'] = id


def profile_session(request):
    return Profile.objects.get(id=request.session.get('perfil'))


# def sesion_perfil(request):
    # perfil_primario= Profile.objects.get(user=request.user,soyPrincipal=True)
    # # sesion_perf = request.session.get('sesion_perfil', perfil_primario)
    # # print(sesion_perf)
    # # return sesion_perf
    # from django.contrib.sessions.backends.db import SessionStore
    # s = SessionStore()
    # s['sesion_perfil'] = perfil_primario.id
    # s['sesion_usuario'] = perfil_primario.user.id
    # s.create()
    # s = SessionStore(session_key=s.session_key)
    # # print(s['sesion_perfil'])

# def sesion_act():
    # from django.contrib.sessions.models import Session
    # s=Session.objects.get(sesion_perfil=1)
    # # print(s)
    # # print(s['sesion_perfil'])
    # # s=session_data

def logout(request):
    do_logout(request)
    return redirect('/')


@login_required
def edit_profile(request):

    instance_profile = Profile.objects.get(user=request.user)
    valido = True

    if request.method == "POST":
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=instance_profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            valido = False
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=instance_profile)

    context = {

        'user_form': user_form,
        'profile_form': profile_form,
        'soyValido': valido
    }
    return render(request, "gestion_usuario/edit_profile.html", context)


@login_required
def profile(request):
    try:
        instance_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        instance_profile = Profile(
            user=request.user, nickname=request.user.username)
        instance_profile.save()

    context = {
        "fecha_nacimiento": instance_profile.fecha_nacimiento,
        "nickname": instance_profile.nickname,
        "soyPrincipal": instance_profile.soyPrincipal
    }
    return render(request, "gestion_usuario/profile.html", context)


def index(request):
    return render(request, "index.html")

