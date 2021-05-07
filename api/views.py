from django.shortcuts import render
from namaka_admin.models import Utente, Borraccia, Sorso
from django.http import HttpResponse
from django.forms.models import model_to_dict
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.core import serializers
import decimal
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


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

            
@csrf_exempt
def getBorracciaLivello(request, id_borraccia):
    if request.method == 'GET':
        try:
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            livello_borraccia = {'livello_attuale': borraccia.livello_attuale}
            return JsonResponse(livello_borraccia)
        except:
            return HttpResponse("La borraccia inserita non esiste")
    if request.method == 'POST':
        try:
            borraccia = Borraccia.objects.get(pk=id_borraccia)
            data = json.loads(request.body)
            borraccia.livello_attuale = data['livello_attuale']
            borraccia.save()
            return HttpResponse(status=200)    
        except:
            return HttpResponse("La borraccia inserita non esiste")
 

@csrf_exempt
def registrazioneUtente(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        try:
            utente = Utente.objects.get(pk=data['username'])
            return HttpResponse(status=404)
        except:
            fabbisogno = (int(data['altezza'])+int(data['peso']))/100
            utente = Utente(email_utente=data['username'], password=data['password'], lat_utente=40.97938647025624, lon_utente=14.20780902936019, fabbisogno=fabbisogno)
            utente.save()
            return HttpResponse(status=200)

@csrf_exempt
def loginUtente(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            utente = Utente.objects.get(pk=data['username'], password=data['password'])
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)


def getAllUser(request):
    if request.method == 'GET':
        try:
            lista_utenti=[]
            utente = Utente.objects.all()
            for u in utente:
                lista_utenti.append(u.email_utente)
            return JsonResponse({'lista_utenti': lista_utenti})
        except:
            return HttpResponse("fallito")

@csrf_exempt
def postTime(request,email_utente):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            utente = Utente.objects.get(pk=email_utente)
            utente.tempo = data['tempo']
            utente.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)
    if request.method == 'GET':
        try:
            utente = Utente.objects.get(pk=email_utente)
            tempo = {'tempo': utente.tempo}
            return JsonResponse(tempo)
        except:
            return HttpResponse("Il tempo non esiste")        

@csrf_exempt
def sorsi(request, email_utente, giorno):
    giorno = datetime.strptime(giorno, '%Y-%m-%d')
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            sorso = Sorso.objects.all()
            for s in sorso:
                if s.giorno == giorno.date() and s.utente.email_utente==email_utente:
                    s.totale = data['totale']
                    s.save()
                    return HttpResponse(status=200)
            try:
                utente = Utente.objects.get(pk=email_utente)
                sorso = Sorso(giorno=giorno.date(), utente=utente, totale=data['totale'])
            except ValueError:
                print("erroreeeee", ValueError) 
            try:
                sorso.save()
                return HttpResponse(status=200)
            except:
                return HttpResponse(status=405)
        except:
            return HttpResponse(status=404)
    
    if request.method == 'GET':
        try:
            sorso = Sorso.objects.all()
            for s in sorso:
                if s.giorno == giorno.date() and s.utente.email_utente==email_utente:
                    totale = {'totale': s.totale}
                    return JsonResponse(totale)
            totale = {'totale': None}
            return JsonResponse(totale)
        except:
            return HttpResponse(status=404)  
