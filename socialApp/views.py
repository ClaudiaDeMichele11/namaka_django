from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from namaka_admin.models import CodiceSconto, Sorso, Invito, Vittorie, Gruppo, User, Group
from django.http import HttpResponse
from datetime import date
import jwt
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

@csrf_exempt
def invita(request):
    if request.method == 'POST':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        data = json.loads(request.body)
       
        try:
            mittente = User.objects.get(email = data['mittente'])
            destinatario = User.objects.get(email = data['destinatario'])
            gruppo = Group.objects.get(name = data['gruppo'])
            gruppi = Gruppo.objects.filter(group=gruppo)
            for g in gruppi:
                if g.creatore.get_username()==data['creatore']:
                    invito2 = Invito(gruppo=g, mittente=mittente, destinatario = destinatario, stato="NON VISUALIZZATO")
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
                invito['gruppo']=i.gruppo.nameGroup
                invito['creatore']=i.gruppo.creatore.get_username()
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
            nomeUff = data['gruppo']+data['creatore']
            gruppoUff = Group.objects.get(name = nomeUff)
            gruppo = Gruppo.objects.filter(group=gruppoUff)
            for g in gruppo:
                invito = Invito.objects.get(gruppo=g,  mittente=mittente, destinatario = destinatario)
                invito.stato = data['stato']
                invito.save()
                if data['stato'] == "ACCETTATO":
                    gruppoUff.user_set.add(destinatario)
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
            g1 = Group.objects.create(name=data['nomeGruppo']+email_utente)
            
            g2 = Gruppo(creatore = creatore, group = g1, nameGroup=data['nomeGruppo'])
            g1.user_set.add(creatore)
            g2.save()
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
                g2 = Gruppo.objects.filter(group=g)
                for v in g2:
                    lista_gruppi.append({'nome': v.nameGroup, 'creatore':v.creatore.get_username()})
            json_stuff={'gruppi': lista_gruppi}
            return JsonResponse(json_stuff)
        except:
            return HttpResponse(status=405)

            
def getPartecipanti(request, nomegruppo, creatore):
    if request.method == 'GET':
        try:
            today = date.today()
            value = checkToken(request)
            if value == 1 :
                return HttpResponse(status=401)
            utenti = User.objects.filter(groups__name=nomegruppo+creatore)
            lista_partecipanti = []
            for u in utenti:
                sorso = Sorso.objects.all()
                trovato = False
                for s in sorso:
                    if s.giorno == today and s.utente.get_username() == u.get_username():
                         lista_partecipanti.append({'nome': u.get_username(), 'totale': s.totale})
                         trovato=True
                if trovato == False:
                    lista_partecipanti.append({'nome': u.get_username(), 'totale': 0})
            newlist = sorted(lista_partecipanti, key=lambda k: k['totale'], reverse=True) 
            
            if len(newlist)==1:
                for e in newlist:
                    e['posizione']=0
                    json_stuff={'partecipanti': [e]}
                    return JsonResponse(json_stuff)
            
            if newlist[0]['totale']==0:
                for e in newlist:
                    e["posizione"] = 0
                json_stuff={'partecipanti': newlist}
                return JsonResponse(json_stuff)
            i=1
            for e in newlist:
                e["posizione"] = i
                i=i+1
            json_stuff={'partecipanti': newlist}
            return JsonResponse(json_stuff)
        except:
            return HttpResponse(status=405)

def check_codice_sconto(numVittorie,email_utente):
    if numVittorie > 5:
        membro = User.objects.get(email = email_utente)
        codici_sconto = CodiceSconto.objects.filter(utente=membro)
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
                    if(v.gruppo.name == gruppo):
                        vittoria = {"giorno": v.giorno.strftime('%Y-%m-%d')}
                        listavittorie.append(vittoria)
            n = check_codice_sconto(len(listavittorie), email_utente)
            json_stuff={'Listavittorie': listavittorie, 'numeroSconti': n}
           
            return JsonResponse(json_stuff)
        except:
            json_stuff={'Listavittorie': [], 'numeroSconti': n}
            return JsonResponse(json_stuff)

def sconti(request,email_utente):
    if request.method == 'GET':
        value = checkToken(request)
        if value == 1 :
            return HttpResponse(status=401)
        membro = User.objects.get(email = email_utente)
        try:
            sconti = CodiceSconto.objects.filter(utente=membro)
            ListaSconti = []
            for s in sconti:
                value = {"valore": s.valore, "codice": s.codice_sconto}
                ListaSconti.append(value)
            json_stuff={'ListaSconti': ListaSconti}
            return JsonResponse(json_stuff)
        except:
            json_stuff={'ListaSconti': []}
            return JsonResponse(json_stuff)

def checkInviti(request, email_utente):
    if request.method == 'GET':
        value = checkToken(request)
        if value == 1 :
           return HttpResponse(status=401)
        inviti = Invito.objects.all()
        new_notifiche = 0
        for i in inviti:
            if i.destinatario.get_username() == email_utente and (i.stato=="NON VISUALIZZATO" or i.stato=="VISUALIZZATO"):
                new_notifiche = new_notifiche+1
        json_stuff={'number': new_notifiche}
        return JsonResponse(json_stuff)

@csrf_exempt
def addCodiciSconto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            nome_codice = data['nome']
            value = data['value']
            c = CodiceSconto(valore=value, codice_sconto=nome_codice)
            c.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)