from namaka_admin.models import  Utente, Borraccia, Sorso, Vittorie
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password

from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import jwt
from datetime import datetime
import datetime
from django.contrib.auth.models import Group
from web_namaka.settings import SECRET_KEY


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
            value = checkToken(request)
            if value == 1 :
                return HttpResponse(status=401)
            utenti=Utente.objects.all()
            lista_utente = []
            for u in utenti:
                if(u.user.get_username() == email_utente):
                    ut = model_to_dict(u)
                    lista_utente.append(ut)
                    f={'utente': lista_utente}
                    return JsonResponse(f)    
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
        return HttpResponse(status=200)

            
@csrf_exempt
def getFabbUtente(request, email_utente):
    if request.method == 'GET':
        try:
            utenti=Utente.objects.all()
            for u in utenti:
                if(u.user.get_username() == email_utente):
                    fabb = u.fabbisogno
                    f={'fabbisogno': fabb}
                    return JsonResponse(f)            
        except:
            return HttpResponse("L'utente inserito non esisteeeeee")
    if request.method == 'POST':
        try:
            value = checkToken(request)
            if value == 1 :
                return HttpResponse(status=401) 
            data = json.loads(request.body)
            u_base = User.objects.get(email=email_utente)
            u = Utente.objects.get(user=u_base)
            u.fabbisogno = float(data['fabbisogno'])
            u.save()
            return HttpResponse(status=200)             
        except:
            return HttpResponse(status=404)    


            

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
        for b in borraccia:
           
            if b.utente.get_username() == email_utente:
                lista_borracce.append(model_to_dict(b))
        json_stuff={'borracce': lista_borracce}
        return JsonResponse(json_stuff)

    if request.method == 'POST':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401) 
        data = json.loads(request.body)
        if len(data['id']) > 0 and len(data['id']) <=2:
            try:
                if Borraccia.objects.filter(id_borraccia=data['id']):
                    return HttpResponse(status=403)
                u = User.objects.get(email = email_utente)
                borraccia = Borraccia(id_borraccia=data['id'], lat_borr=float(data['latitudine']), lon_borr=float(data['longitudine']), capacita=data['capacita'], colore = data['colore'], utente=u)
                borraccia.save()
                return HttpResponse(status=200)
            except:
                return HttpResponse(status=405)
        else:
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
        try:
            u = User.objects.get(username=data['username'])
            return HttpResponse(status=404)
        except:
            try:
                validate_password(data['password'])
                user = User.objects.create_user(data['username'], email=data['username'], password=data['password'])
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
            tempo = {'tempo': None}
            return JsonResponse(tempo)     



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
                    print("Hai vinto")
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
    if request.method == 'POST':
        data = json.loads(request.body)
        sorso = Sorso.objects.all()
        for s in sorso:
            if s.giorno == giorno.date() and s.utente.get_username()==email_utente:
                var = s.totale
                nuovoTotale = var + data['totale']
                s.totale = nuovoTotale
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
                if(u.user.get_username() == email_utente):  
                    fabb = u.fabbisogno         
            sorso = Sorso.objects.all()
            for s in sorso:
                if s.giorno == giorno.date() and s.utente.get_username()==email_utente:
                    info = {'info': [{'fabbisogno': fabb, 'totale': s.totale}]}
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
        try:
            borraccia = Borraccia.objects.all()
            for b in borraccia:
                if b.utente.get_username() == data['user'] and b.id_borraccia == data['id_borraccia']:
                    b.delete()
                    return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)
