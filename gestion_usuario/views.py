from django.shortcuts import render
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def home(request):
    #return render(request,os.path.join(BASE_DIR,'templates','test.html'),{"noticias":[]})
    return render(request,'home.html',{"hola":1})