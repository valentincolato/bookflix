from django.contrib import admin
from django.http import HttpResponseRedirect
import os
from gestion_libro.models import Autor, Genero, Editorial, Libro,Capitulo
from PyPDF2 import PdfFileMerger, PdfFileReader
import random
from .forms import CapituloForm
from django.core.exceptions import ObjectDoesNotExist
# Register your models here.
# Register your models here.
admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Editorial)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    change_form_template = "libro_changeform.html"

    def response_change(self, request, obj):
        if obj.es_capitulado:
            try:
                obj.numero_de_capitulos = request.POST['numero_de_capitulos']
            except:
                pass
        else :
            try:
                try:
                    obj.pdf = request.POST['pdf']
                except:
                    obj.pdf = request.FILES['pdf']
            except:
                pass
        obj.save()
        return super().response_change(request, obj)

    def render_change_form(self, request, context, *args, **kwargs):
        self.change_form_template = "libro_changeform.html"
        libro = context['original']
        try:
            capitulos =Capitulo.objects.filter(libro=libro).order_by('-numero_de_capitulo')
        except ObjectDoesNotExist:
            capitulos =[]

        extra = {'capitulos': capitulos, "libro_id":libro.id, 'libro': libro }
        context.update(extra)



        return super(LibroAdmin, self).render_change_form(request,
                                                            context, *args, **kwargs)


class CapituloAdmin(admin.ModelAdmin):
       list_display = ("numero_de_capitulo", "pdf")

       def get_form(self, request, obj=None, **kwargs):
           if obj.type == "1":
               self.exclude = ("libro", )
           form = super(Capitulo, self).get_form(request, obj, **kwargs)
           return form
