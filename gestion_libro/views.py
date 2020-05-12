from django.shortcuts import render

from .models import Libro
# Create your views here.

def libro_especifico(request,libroId):
	l=Libro.objects.get(id=libroId)
	contexto={"libro":l}
	return render(request, "libroDetalle.html",contexto)
