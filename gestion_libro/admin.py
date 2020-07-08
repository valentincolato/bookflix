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

    def render_change_form(self, request, context, *args, **kwargs):
        self.change_form_template = "libro_changeform.html"
        libro =context['original']
        
        try:
            capitulos =Capitulo.objects.filter(libro=libro).order_by('-numero_de_capitulo')
        except ObjectDoesNotExist:
            capitulos =[]
       
        extra = {'capitulos': capitulos, "libro_id":libro.id}
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