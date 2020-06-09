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

from gestion_usuario.views import profile_session
from gestion_usuario.models import Favorito
# view_pdf
from tika import parser
# proteger


def fotos_libros():
    libros = Libro.objects.all()
    fotos_libros = list(
        map(lambda libro: (libro.id, ((str(libro.foto)).split('static/'))[1]), libros))
    fotos_dict = {}
    for foto_libro in fotos_libros:
        fotos_dict[foto_libro[0]] = foto_libro[1]
    return fotos_dict


def libro_especifico(request, libroId):
    l = Libro.objects.get(id=libroId)
    fav = buscar_fav(request, libroId)
    # Por ahora hasta que se implementen los caps en el modelo
    caps = [5, 10, 16, 19]
    contexto = {"libro": l, "favorito": fav, "capitulos": caps}
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


@login_required
def libros(request):
    context = {"libros": Libro.objects.all(), "estoy_en_home": True,
               "fotos_libros": fotos_libros()}

    return render(request, "libros.html", context)



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

def comparar_string(query,filtro):
    return query in normalize(str(filtro).lower())

def comparar_genero(query,generos):
    return any(comparar_string(query,genero) for genero in generos)

def buscar_libros(filtro, query):

    switcher = {
        "nombre": list(filter(lambda libro: comparar_string(query,libro.nombre), Libro.objects.all())),
        "genero": list(filter(lambda libro: comparar_genero(query,libro.genero.all()), Libro.objects.all())),
        "autor": list(filter(lambda libro: comparar_string(query,libro.autor), Libro.objects.all())),
        "editorial": list(filter(lambda libro: comparar_string(query,libro.editorial), Libro.objects.all())),
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
