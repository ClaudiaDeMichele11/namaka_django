from django.conf import Settings
from django.shortcuts import render
from django.urls.resolvers import URLResolver
from namaka_admin.models import CodiceSconto, Utente, Borraccia, Sorso, Invito, Vittorie
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from django.core import serializers
import decimal
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password

from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import UserManager, User
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta, date
import datetime
import time
import operator

from django.contrib.auth.models import Group



SECRET_KEY = 'django-insecure-fo$-puwh)udlcn!9$acr&1lqa^dy%+0bedu7bu6ju@my+(q^)0'
def checkToken(request):
    jwt_token = request.headers.get('authorization', None)     
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY,
                                 algorithms= 'HS256')
            print("Token di accesso valido")
            return 0
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            print("Token di accesso non valido")
            return 1

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
def refreshToken(request):
    if request.method == 'POST':
        print("Aggiorna Token Accesso mediante refresh")
        data = json.loads(request.body)
        try:
            payload = jwt.decode(data["refresh"], SECRET_KEY, algorithms= 'HS256')
            user = User.objects.get(id=int(payload["user_id"]))
            access = AccessToken.for_user(user)
            response = {
                'access': str(access),
                }
            return JsonResponse(response)
        except:
            print("Il token di refresh è scaduto")
            return HttpResponse(status=401)
            
           

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
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401) 
        data = json.loads(request.body)
        utenti=Utente.objects.all()
        for u in utenti:
            if(u.user.get_username() == email_utente):
                u.lat_utente = data["latitudine"]
                u.lon_utente = data["longitudine"]
                u.save()
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
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
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
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401) 
        data = json.loads(request.body)
        print(data)
        try:
            if Borraccia.objects.filter(id_borraccia=data['id']):
                return HttpResponse(status=403)
            
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
            return HttpResponse(status=404)
        except:
            try:
                validate_password(data['password'])
                user = User.objects.create_user(data['username'], email=data['username'], password=data['password'])
                print("user")
                fabbisogno = (int(float(data['altezza']))+int(float(data['peso'])))/100
                utente = Utente(fabbisogno=fabbisogno, user = user)
                utente.save()
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                print("Access token signup", access)
                print("Refresh token signup", refresh)
                response = {
                    'refresh': str(refresh),
                    'access': str(access),
                    }
                return JsonResponse(response)
            except:
                return HttpResponse(status=405)

    

@csrf_exempt
def loginUtente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            print("L'utente e' registrato!", user)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            print("Access token login", access)
            print("Refre token login", refresh)
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



def checkVittoria(email_utente, giorno, nuovototale):
    membro = User.objects.get(email = email_utente)
    query_set = Group.objects.filter(user = membro)
    for g in query_set:
        vittorie = Vittorie.objects.all()
        check = False
        for v in vittorie:
            if v.giorno == giorno.date() and v.gruppo.name == g.name:
                if v.totale > nuovototale:
                    print("Non hai vinto")
                else:
                    print("hai vinto")
                    v.utente = membro
                    v.totale = nuovototale
                    v.save()
                check = True
        if check != True:
            print("Non c'è nessuna vittoria")
            v = Vittorie(utente=membro, giorno=giorno, gruppo=g, totale = nuovototale)
            v.save()
    return 1










@csrf_exempt
def sorsi(request, email_utente, giorno):
    giorno = datetime.datetime.strptime(giorno, '%Y-%m-%d')
    print(giorno)
    if request.method == 'POST':
        data = json.loads(request.body)
        sorso = Sorso.objects.all()
        print(sorso)
        for s in sorso:
            print(s.giorno)
            print(giorno.date())
            print(s.utente.get_username())
            print(email_utente)
            if s.giorno == giorno.date() and s.utente.get_username()==email_utente:
                print(s.totale)
                var = s.totale
                print(var)
                print(type(var))
                print(data['totale'])
                print(type(data['totale']))
                nuovoTotale = var + data['totale']
                s.totale = nuovoTotale
                print(s.totale)
                s.save()
                checkVittoria(email_utente, giorno, nuovoTotale)
                return HttpResponse(status=200)
        u = User.objects.get(email = email_utente)
        sorso = Sorso(giorno=giorno.date(), utente=u, totale=data['totale'])
        sorso.save()
        checkVittoria(email_utente, giorno,data['totale'])
        return HttpResponse(status=200)
           
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
    giorno = datetime.datetime.strptime(giorno, '%Y-%m-%d')
    if request.method == 'GET':
        try:
            value = checkToken(request)
            if value == 1:
                return HttpResponse(status=401)
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
            return JsonResponse({'borracce': lista_borracce})
        json_stuff={'borracce': lista_borracce}
        return JsonResponse(json_stuff)


@csrf_exempt
def removeBottle(request):
    if request.method == 'POST':
        value = checkToken(request)
        if value == 1:
            return HttpResponse(status=401)
        data = json.loads(request.body)
        print("data", data)
        try:
            borraccia = Borraccia.objects.all()
            for b in borraccia:
                print(b.utente)
                if b.utente.get_username() == data['user'] and b.id_borraccia == data['id_borraccia']:
                    print("ugualeeee", b)
                    b.delete()
                    return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)

@csrf_exempt
def invita(request):
    if request.method == 'POST':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        data = json.loads(request.body)
        print(data)
        try:
            mittente = User.objects.get(email = data['mittente'])
            destinatario = User.objects.get(email = data['destinatario'])
            gruppo = Group.objects.get(name = data['gruppo'])
            print("ciaooo")
            
            invito = Invito.objects.filter(gruppo=gruppo, mittente=mittente, destinatario = destinatario)
            if len(invito) != 0: 
                print("aaaaaaaa", invito)
                return HttpResponse(status=405)
            else:
                invito2 = Invito(gruppo=gruppo, mittente=mittente, destinatario = destinatario, stato="NON VISUALIZZATO")
                invito2.save()
                return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)

def getAllInviti(request, email_utente):
    if request.method == 'GET':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        inviti = Invito.objects.all()
        lista_inviti = []
        for i in inviti:
            invito = {}
            if i.destinatario.get_username() == email_utente:
                invito['mittente']= i.mittente.get_username()
                invito['destinatario']= i.destinatario.get_username()
                invito['gruppo'] = i.gruppo.name
                invito['stato'] = i.stato
                lista_inviti.append(invito)
        json_stuff={'inviti': lista_inviti}
        return JsonResponse(json_stuff)

@csrf_exempt
def modificaStatoInvito(request, email_utente):
    if request.method == 'POST':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        data = json.loads(request.body)
        try:
            destinatario = User.objects.get(email = email_utente)
            mittente = User.objects.get(email = data['mittente']) 
            gruppo = Group.objects.get(name = data['gruppo'])
            invito = Invito.objects.get(gruppo=gruppo,  mittente=mittente, destinatario = destinatario)
            invito.stato = data['stato']
            invito.save()
            if data['stato'] == "ACCETTATO":
                gruppo.user_set.add(destinatario)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)


@csrf_exempt
def creaGruppo(request, email_utente):
    if request.method == 'POST':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        data = json.loads(request.body)
        try:
            creatore = User.objects.get(email = email_utente)
            g1 = Group.objects.create(name = data["nomeGruppo"])
            g1.user_set.add(creatore)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=405)

def getGruppoByUtente(request, email_utente):
    if request.method == 'GET':
        try:
            value = checkToken(request)
            if value == 1 :
                return HttpResponse(status=401)
            membro = User.objects.get(email = email_utente)
            query_set = Group.objects.filter(user = membro)
            lista_gruppi = []
            for g in query_set:
                lista_gruppi.append({'nome': g.name})
            json_stuff={'gruppi': lista_gruppi}
            return JsonResponse(json_stuff)
        except:
            return HttpResponse(status=405)

            
def getPartecipanti(request, nomegruppo):
    if request.method == 'GET':
        try:
            today = date.today()
            print(today)
            value = checkToken(request)
            if value == 1 :
                return HttpResponse(status=401)
            utenti = User.objects.filter(groups__name=nomegruppo)
            print("utentiiii", utenti)
            lista_partecipanti = []
            for u in utenti:
               
                sorso = Sorso.objects.all()
                print("sorsooo", sorso)
                trovato = False
                for s in sorso:
                    print("SORSO DI", s.utente.get_username())
                    print("UTENTE BASE", u.get_username())
                    print(s.giorno)
                    if s.giorno == today and s.utente.get_username() == u.get_username():
                         lista_partecipanti.append({'nome': u.get_username(), 'totale': s.totale})
                         trovato=True
                if trovato == False:
                    lista_partecipanti.append({'nome': u.get_username(), 'totale': 0})
                #print(sorso.totale)
            newlist = sorted(lista_partecipanti, key=lambda k: k['totale'], reverse=True) 
            print(newlist)
                
            i=1
            for e in newlist:
                e["posizione"] = i
                i=i+1
            print(newlist)
            json_stuff={'partecipanti': newlist}
            print("listaaaaaa", json_stuff)
            return JsonResponse(json_stuff)
        except:
            return HttpResponse(status=405)

def check_codice_sconto(numVittorie,email_utente):
    if numVittorie > 5:
        print(numVittorie)
        print(email_utente)
        membro = User.objects.get(email = email_utente)
        codici_sconto = CodiceSconto.objects.filter(utente=membro)
        print(codici_sconto)
        numeroSconti = 0
        n=0
        for c in codici_sconto:
            numeroSconti = numeroSconti +1
        if (5 * numeroSconti) == numVittorie:
            print("Hai ricevuto tutti gli sconti che potevi")
            return numeroSconti   
        else: 
            sconti_da_ottenere = numVittorie // 5
            print(sconti_da_ottenere)
            n =  sconti_da_ottenere - numeroSconti 
            if n == 0:
                print("Non hai ancora diritto ad un altro sconto")
                return sconti_da_ottenere
            else:
                print(n)
                codici_sconto = CodiceSconto.objects.filter(stato="NON ASSEGNATO")
                print(codici_sconto)
                for c in codici_sconto:
                    c.stato = "ASSEGNATO"
                    c.utente = membro
                    c.save()
                    n = n-1
                    if n == 0:
                        break
                print("Hai diritto a un nuovo sconto")  
                return sconti_da_ottenere   
    else:
        print("Non hai diritto a codice sconto")
        return 0

def vittorie (request,email_utente, gruppo):
    if request.method == 'GET':
        giorno = date.today()
        membro = User.objects.get(email = email_utente)
        try:
            vittorie = Vittorie.objects.filter(utente=membro)
            listavittorie = []
            for v in vittorie:
                if(v.giorno != giorno):
                    print(v.gruppo)
                    print(v.giorno)
                    if(v.gruppo.name == gruppo):
                        vittoria = {"giorno": v.giorno.strftime('%Y-%m-%d')}
                        listavittorie.append(vittoria)
            n = check_codice_sconto(len(listavittorie), email_utente)
            json_stuff={'Listavittorie': listavittorie, 'numeroSconti': n}
            print("----------", json_stuff)
            return JsonResponse(json_stuff)
        except:
            json_stuff={'Listavittorie': [], 'numeroSconti': n}
            return JsonResponse(json_stuff)

def sconti(request,email_utente):
    if request.method == 'GET':
        membro = User.objects.get(email = email_utente)
        try:
            sconti = CodiceSconto.objects.filter(utente=membro)
            ListaSconti = []
            for s in sconti:
                value = {"valore": s.valore, "codice": s.codice_sconto}
                ListaSconti.append(value)
            json_stuff={'ListaSconti': ListaSconti}
            print(json_stuff)
            return JsonResponse(json_stuff)
        except:
            json_stuff={'ListaSconti': []}
            print(json_stuff)
            return JsonResponse(json_stuff)