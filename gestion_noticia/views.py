from django.shortcuts import render,redirect
from .models import Noticia

# Create your views here.
def news(request):
	n=Noticia.objects.all()
	contexto={"noticias":n}
	return render(request, "news.html",contexto)

def news_especifica(request,newsId):
	n=Noticia.objects.get(id=newsId)
	contexto={"noticia":n}
	return render(request, "newsEspecifica.html",contexto)