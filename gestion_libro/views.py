from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from .models import Libro, Capitulo
from .forms import CapituloForm
# from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from django.db.models import Q  
from django.views.generic import TemplateView, ListView

from gestion_noticia.models import Noticia, Trailer
from django.contrib.admin.views.decorators import staff_member_required

from gestion_usuario.views import profile_session
from gestion_usuario.models import Favorito, Historial, Comentario, Profile, Leidos,CapitulosLeidos,Puntaje
from gestion_usuario.forms import CommentCreateForm
# view_pdf
from tika import parser
# proteger

from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def termino_libro(request, libro ,capitulos):
	capitulos_terminados = []
	termino_lectura = True
	if libro.es_capitulado:
		for cap in capitulos:
			try:
				termino_capitulo = CapitulosLeidos.objects.get( libro=libro.id,capitulo = cap.id, perfil=request.session['perfil'])
				capitulos_terminados.append(termino_capitulo.capitulo.id)
			except:
				termino_lectura = False
		# Debe haber igual cantidad de capitulos a capitulos leidos
		termino_lectura = termino_lectura and len(capitulos_terminados) == libro.numero_de_capitulos
	else:
		try:
			Leidos.objects.get( libro=libro.id, perfil=request.session['perfil'])
		except:
			termino_lectura = False

	return capitulos_terminados, termino_lectura

def libro_no_disponible(request):
	return render(request, "libronodisponible.html")


def disponibilidad_libro(libro):
	return libro.ocultar == False and (libro.fecha_vencimiento == None or libro.fecha_vencimiento >= date.today())


def libro_especifico(request, libroId):
	l = Libro.objects.get(id=libroId)
	caps = []

	form_comentario = CommentCreateForm()
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
		if l.es_capitulado:
			try:
				caps = Capitulo.objects.filter(libro=l).order_by('numero_de_capitulo')
			except ObjectDoesNotExist:
				caps=[]

		completitud_libro = termino_libro(request, l, caps)
		caps_terminados = completitud_libro[0]
		termino_lectura = completitud_libro[1]

		contexto = {
								"libro": l,
								"favorito": fav,
								"capitulos": caps,
								"comentarios": Comentario.objects.filter(libro=l),
								"form_comentario": form_comentario,
								"termino_lectura": termino_lectura,
								"capitulos_terminados": caps_terminados,
								"porcentaje":porcentaje_likes(libroId),
								"votostotales":cant_likes(libroId),
								"trailers":Trailer.objects.filter(libro=l),
								"disponibilidad":disponibilidad_libro(l),
								"punt": puntuar(request, libroId, None),

							}
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


#fran

def puntuar(request, libroId, puntaje):
	try:
		punt = (Puntaje.objects.get(libro_id=libroId, perfil_id=profile_session(request)))
	except:
		if puntaje == None:
			punt=None
		else:
			l = Libro.objects.get(id=libroId)
			per = profile_session(request)
			punt = Puntaje(libro=l, perfil=per, like= puntaje)
			punt.save()
	return punt

def dar_like(request, libroId):
	puntuar(request, libroId,True)
	return redirect('/libro/'+str(libroId))

def dar_dislike(request, libroId):
	puntuar(request, libroId,False)
	return redirect('/libro/'+str(libroId))
def borrar_puntaje(request, libroId):
	punt=puntuar(request, libroId,True)#feo codigo
	punt.delete()
	return redirect('/libro/'+str(libroId))

def porcentaje_likes(libroId):
	
	all=Puntaje.objects.filter(libro_id=libroId)
	likes=filter(lambda x: x.like==True, all)
	try:
		por= (len(list(likes))/len(list(all))) * 100
	except:
		return 0
	return por
def cant_likes(libroId):
	all=Puntaje.objects.filter(libro_id=libroId)
	return len(list(all))
	

#endFran	
	
	
	
def agregar_a_historial(libroId, perf):
	try:
		his = Historial.objects.get(libro_id=libroId, perfil_id=perf)
	except:
		his = Historial(libro=Libro.objects.get(
			id=libroId), perfil=perf, pagina=1)
	his.save()


#def decodificar_caps(libro):
#	caps = libro.capitulos
#	caps = caps.replace(' ', '')
#	caps = caps.split(',')
#	lista = list(map(lambda x: int(x), filter(lambda y: y.isnumeric(), caps)))
#	print(lista)
#	return lista


def libros_disponibles(libros):
	return list(filter(lambda libro: disponibilidad_libro(libro), libros))


@login_required
def home_logueado(request):

	context = {"libros": libros_disponibles(Libro.objects.all()), "libros_favoritos": Favorito.objects.filter(perfil=request.session['perfil']),
			   "estoy_en_home": True, "noticias": Noticia.objects.all()}

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
	return filter(lambda libro: disponibilidad_libro(libro) ,switcher[filtro]) #Fran


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
	fecha_invalida=False

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
		else:
			fecha_invalida = True

	return render(request, 'admin/informe_libro.html', {"libros": libros_con_visitas, "fecha_invalida":fecha_invalida})


@ staff_member_required
def add_capitulo(request, id_libro):

	libro = Libro.objects.get(id=id_libro)
	ya_existe = False
	superaste_el_maximo = False

	print(request.POST)
	if request.method == "POST":
		form = CapituloForm(request.POST, request.FILES)
		if form.is_valid():
			if int(request.POST['numero_de_capitulo']) <= libro.numero_de_capitulos:
					capitulo = form.save()
					try:

						capitulo_a_subir = Capitulo.objects.get(
							libro=id_libro, numero_de_capitulo=int(request.POST['numero_de_capitulo']))
					except ObjectDoesNotExist:

						capitulo = form.save()
						capitulo.libro = libro

						capitulo.save()
						return HttpResponse('<script type="text/javascript">window.close()</script>')
					ya_existe = True
			else:
				superaste_el_maximo = True
	else:
		form = CapituloForm()

	context = {"form": form,  "ya_existe": ya_existe,
		"superaste_el_maximo": superaste_el_maximo}
	return render(request, 'admin/add_capitulo.html', context)

def existe_cap(numero_de_capitulo,id_capitulo, libro):
	capitulos = Capitulo.objects.filter(libro=libro)
	suma = 0
	for capitulo in capitulos:
		if (int(id_capitulo) != capitulo.id and (capitulo.numero_de_capitulo) == numero_de_capitulo):
			return True

	return False

@ staff_member_required
def edit_capitulo(request, id_capitulo):
	superaste_el_maximo =False
	ya_existe=False

	capitulo = Capitulo.objects.get(id=id_capitulo)
	if request.method == "POST":
		form = CapituloForm(request.POST, request.FILES)


		if form.is_valid():
			if (existe_cap(int(request.POST['numero_de_capitulo']),id_capitulo,capitulo.libro)):
				ya_existe=True
			else:
				if int(request.POST['numero_de_capitulo']) <= capitulo.libro.numero_de_capitulos:
					form.save()
					try:
						capitulo.pdf = request.POST['pdf']
					except:
						capitulo.pdf = request.FILES['pdf']
					capitulo.numero_de_capitulo = int(request.POST['numero_de_capitulo']) 
					capitulo.save()

					return HttpResponse('<script type="text/javascript">window.close()</script>')
				else:
					superaste_el_maximo =True
	else:
		form = CapituloForm(instance=capitulo)

	context = {"form": form,  "ya_existe": ya_existe, "superaste_el_maximo":superaste_el_maximo}

	return render(request, 'admin/edit_capitulo.html',context)
