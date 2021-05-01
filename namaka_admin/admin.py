from django.contrib import admin
from .models import Utente, Borraccia

class BorracciaAdmin(admin.ModelAdmin):
    list_display = ( 'id_borraccia', 'lat_borr', 'lon_borr', 'capacita', 'colore', 'livello_attuale')

class BorracciaInLine(admin.StackedInline):
    model = Borraccia
    extra = 3

class UtenteAdmin(admin.ModelAdmin):
    inlines = [BorracciaInLine]
    list_display = ( 'email_utente', 'lat_utente', 'lon_utente', 'fabbisogno')


admin.site.register(Borraccia, BorracciaAdmin)
admin.site.register(Utente, UtenteAdmin)