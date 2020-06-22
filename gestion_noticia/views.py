from django.shortcuts import render,redirect
from .models import Noticia,Trailer

# Create your views here.
def news(request):
	n= noticias()
	contexto={"noticias":n}
	return render(request, "news.html",contexto)

def news_especifica(request,newsId):
	n=Noticia.objects.get(id=newsId)
	contexto={"noticia":n}
	return render(request, "newsEspecifica.html",contexto)

def noticias():
	n=Noticia.objects.all().order_by('-fecha_de_creacion')

	return n

def ultimas_noticias(n):
	noticias=Noticia.objects.order_by('-fecha_de_creacion')[0:n]
	return noticias

def trailer(request):
	trailers=Trailer.objects.order_by('-fecha_de_creacion')
	contexto={"trailers":trailers}
	return render(request, "trailer.html",contexto)

def trailer_especifico(request,trailerId):
	trailer=Trailer.objects.get(id=trailerId)
	contexto={"trailer":trailer}
	return render(request, "trailerEspecifico.html",contexto)
