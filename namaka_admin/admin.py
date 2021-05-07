from django.contrib import admin
from .models import Utente, Borraccia, Sorso

class BorracciaAdmin(admin.ModelAdmin):
    list_display = ( 'id_borraccia', 'lat_borr', 'lon_borr', 'capacita', 'colore', 'livello_attuale')

class SorsoAdmin(admin.ModelAdmin):
    list_display = ( 'id_sorso', 'giorno', 'totale')

class SorsoInLine(admin.StackedInline):
    model = Sorso
    extra = 3

class BorracciaInLine(admin.StackedInline):
    model = Borraccia
    extra = 3

class UtenteAdmin(admin.ModelAdmin):
    inlines = [BorracciaInLine, SorsoInLine]
    list_display = ( 'email_utente', 'lat_utente', 'lon_utente', 'fabbisogno', 'tempo')


admin.site.register(Borraccia, BorracciaAdmin)
admin.site.register(Utente, UtenteAdmin)
admin.site.register(Sorso, SorsoAdmin)