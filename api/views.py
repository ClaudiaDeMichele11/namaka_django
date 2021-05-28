from django.conf import Settings
from django.shortcuts import render
from namaka_admin.models import Utente, Borraccia, Sorso
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from django.core import serializers
import decimal
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import UserManager, User
from django.contrib.auth import authenticate
import jwt


def getInfoUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utenti=Utente.objects.all()
            for u in utenti:
                print(u.user.get_username())
                if(u.user.get_username() == email_utente):
                    ut = model_to_dict(u)
                    return JsonResponse(ut)
            return HttpResponse("L'utente inserito non esiste")
        except:
            return HttpResponse("L'utente inserito non esiste")
            
@csrf_exempt
def PosUtente(request, email_utente):
    if request.method == 'GET':
        try:
            print("Helloo")
            utenti=Utente.objects.all()
            for u in utenti:
                print(u.user.get_username())
                if(u.user.get_username() == email_utente):
                    lat = u.lat_utente
                    lon = u.lon_utente
                    pos={'latitudine': lat, 'longitudine': lon}
                    return JsonResponse(pos)
            return HttpResponse("L'utente inserito non esiste")         
        except:
            return HttpResponse("L'utente inserito non esiste")
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Data", data)
        return HttpResponse(status=200)

            

def getFabbUtente(request, email_utente):
    if request.method == 'GET':
        try:
            print("Helloo")
            utenti=Utente.objects.all()
            for u in utenti:
                print(u.user.get_username())
                if(u.user.get_username() == email_utente):
                    fabb = u.fabbisogno
                    f={'fabbisogno': fabb}
                    return JsonResponse(f)            
        except:
            return HttpResponse("L'utente inserito non esisteeeeee")

            

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
            utente = User.objects.get(email = email_utente)
        except:
            return HttpResponse("L'utente inserito non è valido")
        borraccia = Borraccia.objects.all()
        lista_borracce = []
        print("Hello")
        for b in borraccia:
            print(b.utente)
            if b.utente.get_username() == email_utente:
                lista_borracce.append(model_to_dict(b))
        json_stuff={'borracce': lista_borracce}
        return JsonResponse(json_stuff)

    if request.method == 'POST':
        #print(request.headers['Authorization'])
        #token = AccessToken(request.headers['Authorization'])
        """
        token = request.headers['Authorization']
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY,
                                     algorithms= 'HS256')
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return HttpResponse(status=401)

        #print(token)
        """
        data = json.loads(request.body)
        print(data)
        try:
            u = User.objects.get(email = email_utente)
            borraccia = Borraccia(id_borraccia=data['id'], lat_borr=float(data['latitudine']), lon_borr=float(data['longitudine']), capacita=data['capacita'], colore = data['colore'], utente=u)
            borraccia.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)

        
        
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
        print("data", data)
        try:
            u = User.objects.get(username=data['username'])
            print("")
            return HttpResponse(status=404)
        except:
            user = User.objects.create_user(data['username'], email=data['username'], password=data['password'])
            print("user")
            fabbisogno = (int(float(data['altezza']))+int(float(data['peso'])))/100
            utente = Utente(fabbisogno=fabbisogno, user = user)
            utente.save()
            return HttpResponse(status=200)
    

@csrf_exempt
def loginUtente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            print("L'utente e' registrato!")
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(access),
                }
            return JsonResponse(response)
        else:
            print("L'utente non e' registrato!")
            return HttpResponse(status=404)


def getAllUser(request):
    if request.method == 'GET':
        try:
            lista_utenti=[]
            utente = Utente.objects.all()
            print(utente)
            for u in utente:
                lista_utenti.append(u.user.get_username())
            return JsonResponse({'lista_utenti': lista_utenti})
        except:
            return HttpResponse("fallito")

@csrf_exempt
def postTime(request,email_utente):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            utente = Utente.objects.all()
            print(utente)
            for u in utente:
                if(u.user.get_username() == email_utente):
                    u.tempo = data['tempo']
                    u.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)
    if request.method == 'GET':
        try:
            utente = Utente.objects.all()
            for u in utente:
                if(u.user.get_username() == email_utente):
                    tempo = {'tempo': u.tempo}
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
            print("sorsooo", sorso)
            for s in sorso:
                if s.giorno == giorno.date() and s.utente.get_username()==email_utente:
                    s.totale = data['totale']
                    s.save()
                    return HttpResponse(status=200)
            try:
                utenti=Utente.objects.all()
                for u in utenti:
                    print(u.user.get_username())
                    if(u.user.get_username() == email_utente):  
                        sorso = Sorso(giorno=giorno.date(), utente=u, totale=data['totale'])
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
                if s.giorno == giorno.date() and s.utente.get_username()==email_utente:
                    totale = {'totale': s.totale}
                    return JsonResponse(totale)
            totale = {'totale': None}
            return JsonResponse(totale)
        except:
            return HttpResponse(status=404)  

def getInfoGrafico(request, email_utente, giorno):
    giorno = datetime.strptime(giorno, '%Y-%m-%d')
    if request.method == 'GET':
        try:
            utenti=Utente.objects.all()
            for u in utenti:
                print(u.user.get_username())
                if(u.user.get_username() == email_utente):  
                    fabb = u.fabbisogno
                    print("fabb", fabb)            
            sorso = Sorso.objects.all()
            for s in sorso:
                if s.giorno == giorno.date() and s.utente.get_username()==email_utente:

                    info = {'info': [{'fabbisogno': fabb, 'totale': s.totale}]}
                    print("info", info)
                    return JsonResponse(info)
            info = {'info': [{'fabbisogno': fabb, 'totale': 0}]}

            return JsonResponse(info)            
        except:
            info = {'info': [{'fabbisogno': 0, 'totale': 0}]}
            return JsonResponse(info)


def getAllPositionBorracce(request, email_utente):
    if request.method == 'GET':

        borraccia = Borraccia.objects.all()
        lista_borracce = []
        for b in borraccia:
            if b.utente.get_username() == email_utente:
                lista_borracce.append({"coordinates": {"latitude": float(b.lat_borr), "longitude": float(b.lon_borr)}, "title": b.id_borraccia})
        if lista_borracce == []:
            #return HttpResponse("L'utente inserito non ha borracce associate")
            return JsonResponse({'borracce': 0})
        json_stuff={'borracce': lista_borracce}
        return JsonResponse(json_stuff)