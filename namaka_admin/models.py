from django.db import models
from django.contrib.auth.models import User, Group

class Utente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    lat_utente = models.DecimalField(max_digits=16, decimal_places=14, null=True)
    lon_utente = models.DecimalField(max_digits=16, decimal_places=14, null=True)
    fabbisogno = models.FloatField()
    tempo = models.DateTimeField(default=None, null=True)


class Gruppo(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True)
    creatore=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    nameGroup = models.CharField(primary_key=True, max_length = 10)

class Borraccia(models.Model):
    
    id_borraccia = models.CharField(primary_key=True, max_length = 2)
    lat_borr = models.DecimalField(max_digits=16, decimal_places=14, default=0)
    lon_borr = models.DecimalField(max_digits=16, decimal_places=14, default=0)
    capacita = models.IntegerField(default=0)
    colore = models.TextField(max_length=15, default=None)
    livello_attuale = models.IntegerField(default=0)
    utente = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    

class Sorso(models.Model):
    id_sorso = models.AutoField(primary_key=True)
    giorno = models.DateField(default=None)
    totale = models.IntegerField(default=0)
    utente = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Vittorie(models.Model):
    codice_vittoria = models.AutoField(primary_key=True)
    giorno = models.DateField(default=None)
    utente = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    gruppo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    totale = models.IntegerField(default=0)


class CodiceSconto(models.Model):
    class statoSconto(models.TextChoices):
        ASSEGNATO = 'ASSEGNATO', 
        NON_ASSEGNATO = 'NON ASSEGNATO', 
        
    codice_sconto = models.AutoField(primary_key=True)
    valore = models.IntegerField(default=25)
    stato = models.CharField(choices=statoSconto.choices, default=statoSconto.NON_ASSEGNATO, max_length=20)
    utente = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    

class Invito(models.Model):
    class statoInvito(models.TextChoices):
        VISUALIZZATO = 'VISUALIZZATO', 
        NON_VISUALIZZATO = 'NON VISUALIZZATO', 
        ACCETTATO = 'ACCETTATO', 
        RIFIUTATO = 'RIFIUTATO'

    id_invito = models.AutoField(primary_key=True, default=None)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, )
    mittente = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='mittente')
    stato = models.CharField(choices=statoInvito.choices, default=statoInvito.NON_VISUALIZZATO, max_length=20)
    gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, null=True)
