from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework_jwt.views import verify_jwt_token


app_name = 'api'

urlpatterns = [
    path('utente/<str:email_utente>', views.getInfoUtente, name='getInfoUtente'),
    path('utenteposizione/<str:email_utente>', views.PosUtente, name='PosUtente'),
    path('utentefabb/<str:email_utente>', views.getFabbUtente, name='getFabbUtente'),
    path('borracciaInfo/<str:id_borraccia>', views.getInfoBorraccia, name='getInfoBorraccia'),
    path('borracciaprop/<str:email_utente>', views.getBorracceUtente, name='getBorracceUtente'),
    path('borraccia/<str:email_utente>/<str:id_borraccia>', views.getInfoBorraccia, name='getInfoBorraccia'),
    path('borracciaPos/<str:id_borraccia>', views.getBorracciaPosizione, name='getBorracciaPosizione'),
    path('borracciaLivello/<str:id_borraccia>', views.getBorracciaLivello, name='getBorracciaLivello'),
    path('registrazione', views.registrazioneUtente, name='registrazioneUtente'),
    path('login', views.loginUtente, name='loginUtente'),
    path('getutenti', views.getAllUser, name='getAllUser'),
    path('postTime/<str:email_utente>', views.postTime, name='postTime'),
    path('sorsi/<str:email_utente>/<str:giorno>', views.sorsi, name='sorsi'),
    path('grafico/<str:email_utente>/<str:giorno>', views.getInfoGrafico, name='getInfoGrafico'),    
    path('allposition/<str:email_utente>', views.getAllPositionBorracce, name='getAllPositionBorracce'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    
    
    
]
