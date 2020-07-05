from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from .models import Libro
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from django.db.models import Q  # new
from django.views.generic import TemplateView, ListView
# Create your views here.
from gestion_noticia.models import Noticia
from django.contrib.admin.views.decorators import staff_member_required

from gestion_usuario.views import profile_session
from gestion_usuario.models import Favorito, Historial, Comentario, Profile, Leidos
from gestion_usuario.forms import CommentCreateForm
# view_pdf
from tika import parser
# proteger

from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def fotos_libros():
    libros = Libro.objects.all()
    fotos_libros = list(
        map(lambda libro: (libro.id, ((str(libro.foto)).split('static/'))[1]), libros))
    fotos_dict = {}
    for foto_libro in fotos_libros:
        fotos_dict[foto_libro[0]] = foto_libro[1]
    return fotos_dict


def libro_no_disponible(request):
    return render(request, "libronodisponible.html")


def disponibilidad_libro(libro):
    return libro.ocultar == False and (libro.fecha_vencimiento == None or libro.fecha_vencimiento >= date.today())


def libro_especifico(request, libroId):
    l = Libro.objects.get(id=libroId)

    try:
        termino_lectura = Leidos.objects.get(libro=l.id, perfil=request.session['perfil'])
        termino_lectura = True
    except ObjectDoesNotExist:
        termino_lectura = False

    form_comentario = CommentCreateForm()
    if disponibilidad_libro(l) == False:
        return redirect('/libronodisponible')
    else:
        if request.method == "POST":
            form_comentario = CommentCreateForm(data=request.POST)
            if form_comentario.is_valid():

                comentario = form_comentario.save()
                comentario.perfil = Profile.objects.get(
                    id=request.session['perfil'])
                comentario.libro = l
                comentario.save()

        fav = buscar_fav(request, libroId)
        agregar_a_historial(libroId, profile_session(request))
        caps = decodificar_caps(l)
        contexto = {"libro": l, "favorito": fav, "capitulos": caps,
                    "comentarios": Comentario.objects.filter(libro=l), "form_comentario": form_comentario, "termino_lectura": termino_lectura}
    return render(request, "libroDetalle.html", contexto)


def buscar_fav(request, libroId):
    try:
        fav = (Favorito.objects.get(libro_id=libroId,
                                    perfil_id=profile_session(request)))
    except:
        fav = None
    return fav

# proteger


def libro_fav(request, libroId):
    fav = buscar_fav(request, libroId)
    if fav != None:
        fav.delete()
    else:
        l = Libro.objects.get(id=libroId)
        per = profile_session(request)
        fav = Favorito(libro=l, perfil=per)
        fav.save()
    return redirect('/libro/'+str(libroId))


def agregar_a_historial(libroId, perf):
    try:
        his = Historial.objects.get(libro_id=libroId, perfil_id=perf)
    except:
        his = Historial(libro=Libro.objects.get(
            id=libroId), perfil=perf, pagina=1)
    his.save()


def decodificar_caps(libro):
    caps = libro.capitulos
    caps = caps.replace(' ', '')
    caps = caps.split(',')
    lista = list(map(lambda x: int(x), filter(lambda y: y.isnumeric(), caps)))
    print(lista)
    return lista


def libros_disponibles(libros):
    return list(filter(lambda libro: disponibilidad_libro(libro), libros))


@login_required
def home_logueado(request):

    context = {"libros": libros_disponibles(Libro.objects.all()), "libros_favoritos": Favorito.objects.filter(perfil=request.session['perfil']),
               "estoy_en_home": True,
               "fotos_libros": fotos_libros(), "noticias": Noticia.objects.all()}

    return render(request, "home_logueado.html", context)


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def comparar_string(query, filtro):
    return query in normalize(str(filtro).lower())


def comparar_genero(query, generos):
    return any(comparar_string(query, genero) for genero in generos)


def buscar_libros(filtro, query):
    # tuve que meter este if en este metodo porque si lo hacia en SearchResultsViews daba error de sintaxis no entiendo porque pero gueno
    if len(query) == 0:
        return None
    else:
        switcher = {
            "nombre": list(filter(lambda libro: comparar_string(query, libro.nombre), Libro.objects.all())),
            "genero": list(filter(lambda libro: comparar_genero(query, libro.genero.all()), Libro.objects.all())),
            "autor": list(filter(lambda libro: comparar_string(query, libro.autor), Libro.objects.all())),
            "editorial": list(filter(lambda libro: comparar_string(query, libro.editorial), Libro.objects.all())),
        }
    return switcher[filtro]


class SearchResultsView(ListView):
    model = Libro
    template_name = 'search.html'

    def get_context_data(self, *args, **kwargs):

        query = self.request.GET['q']
        filtro = self.request.GET['filter']

        context = {"libros": buscar_libros(filtro, normalize(query.lower())),
                   "filtro": filtro}

        return context


def cantidad_vistas(libro):

    return int(len(Historial.objects.filter(libro=libro)))


@ staff_member_required
def informe_libro(request):
    # falta terminar copy paste de informe_usuario por ahora
    libros_con_visitas = []

    if request.method == 'POST':

        fecha_inicio = request.POST['fechaDesde']
        fecha_fin = request.POST['fechaHasta']
        if (fecha_inicio <= fecha_fin):
            historiales = list(filter(lambda historial: (str(historial.fecha.strftime("%Y-%m-%d")) >= str(fecha_inicio)
                                                         and (str(historial.fecha.strftime("%Y-%m-%d")) <= str(fecha_fin))), Historial.objects.all()))

            libros = list(map(lambda historial: (
                historial.libro), historiales))

            libros_ordenados = sorted(
                set(libros), reverse=True, key=lambda libro: cantidad_vistas(libro))

            libros_con_visitas = list(
                map(lambda libro: (libro, cantidad_vistas(libro.id)), libros_ordenados))

    return render(request, 'admin/informe_libro.html', {"libros": libros_con_visitas})
