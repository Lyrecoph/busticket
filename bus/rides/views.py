from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def trajets(request):
    return HttpResponse('Liste des trajets')
