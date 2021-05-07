from django.db import models

class Utente(models.Model):
    email_utente = models.EmailField(max_length=254, primary_key=True)
    lat_utente = models.DecimalField(max_digits=16, decimal_places=14)
    lon_utente = models.DecimalField(max_digits=16, decimal_places=14)
    fabbisogno = models.FloatField()
    password = models.CharField(max_length=50, default=None)
    #borraccia = models.ForeignKey(Borraccia, on_delete=models.CASCADE)
    tempo = models.DateTimeField(default=None)

class Borraccia(models.Model):
    id_borraccia = models.CharField(primary_key=True, max_length=2)
    lat_borr = models.DecimalField(max_digits=16, decimal_places=14, default=0)
    lon_borr = models.DecimalField(max_digits=16, decimal_places=14, default=0)
    capacita = models.IntegerField(default=0)
    colore = models.CharField(max_length=15, default=None)
    livello_attuale = models.IntegerField(default=0)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, default=None)
    

class Sorso(models.Model):
    id_sorso = models.AutoField(primary_key=True)
    giorno = models.DateField(default=None)
    totale = models.IntegerField(default=0)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, default=None)

