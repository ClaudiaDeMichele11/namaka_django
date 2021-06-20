from django.contrib import admin
from django.urls import path
from . import views


app_name = 'socialApp'

urlpatterns = [

    path('invita', views.invita, name='invita'),
    path('inviti/<str:email_utente>', views.getAllInviti, name='getAllInviti'),
    path('checkinviti/<str:email_utente>', views.checkInviti, name='checkInviti'),
    path('modificaStatoInvito/<str:email_utente>', views.modificaStatoInvito, name='modificaStatoInvito'),
    path('creaGruppo/<str:email_utente>', views.creaGruppo, name='creaGruppo'),
    path('getGruppoByUtente/<str:email_utente>', views.getGruppoByUtente, name='getGruppoByUtente'),
    path('getPartecipanti/<str:nomegruppo>/<str:creatore>', views.getPartecipanti, name='getPartecipanti'),
    path('vittorie/<str:email_utente>/<str:gruppo>', views.vittorie, name = 'vittorie'),
    path('sconti/<str:email_utente>', views.sconti, name = 'sconti'),
    path('addCodiciSconto', views.addCodiciSconto, name = 'addCodiciSconto')

]