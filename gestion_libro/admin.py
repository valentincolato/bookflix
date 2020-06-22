from django.contrib import admin
from django.http import HttpResponseRedirect
import os
from gestion_libro.models import Autor,Genero,Editorial,Libro
from PyPDF2 import PdfFileMerger, PdfFileReader
import random

# Register your models here.
# Register your models here.
admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Editorial)
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
	change_form_template = "libro_changeform.html"
	def response_change(self, request, obj):
		if "_make-unique" in request.POST:
			self.agregar_cap(request,obj)
			return HttpResponseRedirect(".")
		return super().response_change(request, obj)
	def agregar_cap(self,request,libro):

		pdfPrincipal= libro.pdf
		nuevoCap= libro.nuevo_capitulo
		if pdfPrincipal and nuevoCap:
			merger = PdfFileMerger()
			merger.append(pdfPrincipal)
			merger.append(nuevoCap)
			random_num=str(random.randint(1,100000))
			merger.write('static/pdf/' + libro.nombre + random_num +  '.pdf')
			libro.pdf='static/pdf/' + libro.nombre+ random_num + '.pdf'
			libro.nuevo_capitulo=None
			merger.close()
			libro.save()
			self.message_user(request, "Capítulo agregado.")
		elif nuevoCap:
			libro.pdf=nuevoCap
			libro.nuevo_capitulo=None
			libro.save()
			self.message_user(request, "El nuevo capitulo ha estrenado tu libro!" )
		else:
			self.message_user(request, "No se puedo agregar capitulo")
