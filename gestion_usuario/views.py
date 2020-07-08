from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserCreationFormExtends, UserEditForm, ProfileEditForm, ProfileCreateForm
from django.contrib.auth.models import User
from .models import Profile, Historial, Comentario,Leidos
from django.shortcuts import get_object_or_404
import os
import random
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from gestion_noticia.views import noticias, ultimas_noticias
from gestion_pago.models import Tarjeta
from gestion_libro.models import Libro,Capitulo
from .models import  CapitulosLeidos
from django.http import HttpResponse, HttpResponseRedirect
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
# @login_required(login_url="/login")


def home(request):
    if request.user.is_authenticated:
        try:
            request.session['perfil']
        except KeyError:
            create_session(request)

        return redirect('home/')

    context = {"estoy_en_home": True, "noticias": ultimas_noticias(3)}
    return render(request, "home.html", context)


# Para los usuarios no logueados
def welcome(request):
    if request.user.is_authenticated:
        return render(request, "gestion_usuario/welcome.html")
    return redirect('/login')


def foto_perfil_random():
    return str(random.randrange(1, 6))


def register(request):
    form = UserCreationFormExtends()

    if request.method == "POST":
        form = UserCreationFormExtends(data=request.POST)
        if form.is_valid():
            user = form.save()
            prf = Profile(user=user, nickname=user.username, soyPrincipal=True)
            prf.foto = 'static/foto_perfil/'+foto_perfil_random()+'.jpg'
            prf.save()

            # creo objeto tarjeta cualquiera hay que modificar esto en el futuro
            tarj = Tarjeta(user=user, numero='1234567', cvc='11')
            tarj.save()
            if user is not None:
                do_login(request, user)
                create_session(request)
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
    request.session['nickname'] = (
        Profile.objects.get(id=perfil_primario.id)).nickname


def change_session_profile(request, id):
    request.session['perfil'] = id
    request.session['nickname'] = (Profile.objects.get(id=id)).nickname

    return redirect('/')


def profile_session(request):
    return Profile.objects.get(id=request.session.get('perfil'))


def desactivar_perfil(request, id):

    profile = Profile.objects.get(id=id)
    if profile.soyPrincipal:
        url = '/profile'
        resp_body = '<script>alert("No se puede desactivar el perfil principal");\
             window.location="%s"</script>' % url

        return HttpResponse(resp_body)
    else:
        profile.user = None
        profile.save()
        profile = Profile.objects.get(user=request.user, soyPrincipal=True)
        request.session['perfil'] = profile.id
        request.session['nickname'] = profile.nickname
        return redirect('/change_profile')

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
    request.session['perfil'] = None
    return redirect('/')


@login_required
def edit_profile(request):

    instance_profile = profile_session(request)
    valido = True

    if request.method == "POST":
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=instance_profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile')

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
        instance_profile = profile_session(request)
    except ObjectDoesNotExist:
        instance_profile = Profile(
            user=request.user, nickname=request.user.username)
        instance_profile.save()

    context = {
        "fecha_nacimiento": instance_profile.fecha_nacimiento,
        "nickname": instance_profile.nickname,
        "soyPrincipal": instance_profile.soyPrincipal,
        "foto_perfil": instance_profile.foto
    }
    return render(request, "gestion_usuario/profile.html", context)




@login_required
def change_profile_view(request):
    perfiles = Profile.objects.filter(user=request.user)
    context = {"estoy_en_home": True, "perfiles": perfiles}
    return render(request, "gestion_usuario/change_profile.html", context)


@login_required
def register_profile(request):
    cant_profiles = len(Profile.objects.filter(user=request.user))
    tipo_suscripcion = (Tarjeta.objects.get(
        user=request.user)).tipo_suscripcion
    if ((tipo_suscripcion.lower() == 'regular' and cant_profiles < 2) or (tipo_suscripcion.lower() == 'premium' and cant_profiles < 4)):
        form = ProfileCreateForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                profile = form.save()
                profile.user = request.user
                if profile.foto == 'static/foto_perfil/default.jpg':
                    profile.foto = 'static/foto_perfil/'+foto_perfil_random()+'.jpg'

                profile.save()
                return redirect('/change_profile/', profile.id)

        return render(request, "gestion_usuario/register_profile.html", {'form': form})
    else:
        url = '/'
        resp_body = '<script>alert("No se pueden agregar mas perfiles se supero el maximo");\
                        window.location="%s"</script>' % url

        return HttpResponse(resp_body)


@login_required
def historial(request):
    context = {"historiales": (Historial.objects.filter(
        perfil=request.session['perfil']).order_by('-fecha'))}

    return render(request, "historial.html", context)


def index(request):
    return render(request, "index.html")


@staff_member_required
def informe_usuario(request):
    usuarios = []
    fecha_invalida=False
    if request.method == 'POST':
        print(request.POST)

        fecha_inicio = request.POST['fechaDesde']
        fecha_fin = request.POST['fechaHasta']
        if (fecha_inicio <= fecha_fin):
            usuarios = list(filter(lambda usuario: (str(usuario.date_joined.strftime("%Y-%m-%d")) >= str(fecha_inicio)
                                                    and (str(usuario.date_joined.strftime("%Y-%m-%d")) <= str(fecha_fin))), User.objects.all()))
        else: 
            fecha_invalida=True

    return render(request, 'admin/informe_usuario.html', {"usuarios": usuarios, "fecha_invalida":fecha_invalida})


@login_required
def borrar_comentario(request, id):

    comentario = Comentario.objects.get(id=id)
    comentario.libro = None
    comentario.perfil = None
    comentario.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def terminar_lectura(request, libro_id):
    
    try:
        lectura = Leidos.objects.get(libro=libro_id,perfil=request.session['perfil'])
    except ObjectDoesNotExist:
        lectura = Leidos()
        lectura.libro = Libro.objects.get(id=libro_id)
        lectura.perfil =  Profile.objects.get(id=request.session['perfil'])
        lectura.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def terminar_capitulo(request, id_libro):
    libro = Libro.objects.get(id=id_libro)
    esta_disponible= True
    try:
    
        capitulos_leidos = CapitulosLeidos.objects.get(libro=libro,perfil=request.session['perfil'])
    except ObjectDoesNotExist:
        capitulos_leidos = CapitulosLeidos()
        capitulos_leidos.libro= libro
        capitulos_leidos.perfil= Profile.objects.get(id=request.session['perfil'])
        capitulos_leidos.numero_capitulo_leido=1
        capitulos_leidos.save()
    
    #esta_disponible el pdf del capitulo?
    try:
        capitulo = Capitulo.objects.get(numero_de_capitulo = capitulos_leidos.numero_capitulo_leido, libro = libro)
    except ObjectDoesNotExist:
        esta_disponible=False
        
    
    esta_disponible= (esta_disponible) and (capitulo.pdf) != ''
           
    if not esta_disponible:
        url = request.META.get('HTTP_REFERER')
        resp_body = '<script>alert("No se puede terminar la lectura del capitulo porque no esta disponible");\
                        window.location="%s"</script>' % url

        return HttpResponse(resp_body)
        

    if capitulos_leidos.numero_capitulo_leido < libro.numero_de_capitulos:
        capitulos_leidos.numero_capitulo_leido +=1
   
   
    capitulos_leidos.save()
    if capitulos_leidos.numero_capitulo_leido == libro.numero_de_capitulos:
        return redirect('/libro/terminar_lectura/%s' % str(id_libro))




    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))