from django.shortcuts import render
from namaka_admin.models import Utente, Borraccia
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from django.core import serializers
import decimal
from django.views.decorators.csrf import csrf_exempt


def getInfoUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utente = Utente.objects.get(pk=email_utente)
            ut = model_to_dict(utente)
            return JsonResponse(ut)
        except:
            return HttpResponse("L'utente inserito non esiste")
            

def getPosUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utente = Utente.objects.get(pk=email_utente)
            lat = utente.lat_utente
            lon = utente.lon_utente
            pos={'latitudine': lat, 'longitudine': lon}
            return JsonResponse(pos)            
        except:
            return HttpResponse("L'utente inserito non esiste")

            

def getFabbUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utente = Utente.objects.get(pk=email_utente)
            fabb = utente.fabbisogno
            f={'fabbisogno': fabb}
            return JsonResponse(f)            
        except:
            return HttpResponse("L'utente inserito non esiste")

            

def getInfoBorraccia(request, id_borraccia):
    if request.method == 'GET':
        try:
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            b = model_to_dict(borraccia)
            return JsonResponse(b)
        except:
            return HttpResponse("La borraccia inserita non esiste")

            

@csrf_exempt
def getBorracceUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utente = Utente.objects.get(pk=email_utente)
        except:
            return HttpResponse("L'utente inserito è valido")
        borraccia = Borraccia.objects.all()
        lista_borracce = []
        for b in borraccia:
            if b.utente.email_utente == email_utente:
                lista_borracce.append(model_to_dict(b))
            else:
                return HttpResponse("L'utente inserito non ha borracce associate")
        json_stuff={'borracce': lista_borracce}
        return JsonResponse(json_stuff)

    else:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", request.body)
        return HttpResponse("ciaaaaaaaaaao")

        
        
def getBorracciaPosizione(request, id_borraccia):
    if request.method == 'GET':
        try:
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            pos_borraccia = {'latitudine': borraccia.lat_borr, 'longitudine': borraccia.lon_borr}
            return JsonResponse(pos_borraccia)
        except:
            return HttpResponse("La borraccia inserita non esiste")

            

def getBorracciaLivello(request, id_borraccia):
    if request.method == 'GET':
        try:
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            livello_borraccia = {'livello:attuale': borraccia.livello_attuale}
            return JsonResponse(livello_borraccia)
        except:
            return HttpResponse("La borraccia inserita non esiste")
 
@csrf_exempt
def registrazioneUtente(request):
    if request.method == 'POST':
        print("aaaaaa", request.body)
        return HttpResponse("ciaaaaaaaaaao")

