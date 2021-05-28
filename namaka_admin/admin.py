from django.contrib import admin
from .models import Utente, Borraccia, Sorso
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

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


class UtenteAdmin(admin.StackedInline):
    model = Utente
    extra = 3

class UserAdmin(BaseUserAdmin):
    inlines = [UtenteAdmin, BorracciaInLine, SorsoInLine]

"""
class UtentAdmin(admin.ModelAdmin):
    inlines = [BorracciaInLine, SorsoInLine]
    #list_display = ( 'email_utente', 'lat_utente', 'lon_utente', 'fabbisogno', 'tempo')
    list_display = ('lat_utente', 'lon_utente', 'fabbisogno', 'tempo')
"""
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Borraccia, BorracciaAdmin)
#admin.site.register(Utente, UtentAdmin)
admin.site.register(Sorso, SorsoAdmin)