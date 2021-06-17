from django.contrib import admin
from .models import Utente, Borraccia, Sorso , Invito, Vittorie , CodiceSconto, Gruppo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group



class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0

class GenericGroup(GroupAdmin):
    inlines = [UserInLine]

class BorracciaAdmin(admin.ModelAdmin):
    list_display = ( 'id_borraccia', 'lat_borr', 'lon_borr', 'capacita', 'colore', 'livello_attuale')

class InvitoAdmin(admin.ModelAdmin):
    list_display = ( 'destinatario', 'mittente', 'stato', 'gruppo')


class SorsoAdmin(admin.ModelAdmin):
    list_display = ( 'id_sorso', 'giorno', 'totale')

class VittoriaAdmin(admin.ModelAdmin):
    list_display = ( 'codice_vittoria', 'giorno', 'totale', 'gruppo', 'utente')




class CodiceScontoAdmin(admin.ModelAdmin):
    list_display = ( 'codice_sconto', 'valore', 'stato', 'utente')

class SorsoInLine(admin.StackedInline):
    model = Sorso
    extra = 3

class BorracciaInLine(admin.StackedInline):
    model = Borraccia
    extra = 3

class InvitoInLine(admin.StackedInline):
    model = Invito
    fk_name = 'mittente'
    extra = 3

class UtenteAdmin(admin.StackedInline):
    model = Utente
    extra = 3

class UserAdmin(BaseUserAdmin):
    inlines = [UtenteAdmin, BorracciaInLine, SorsoInLine, InvitoInLine]

class GruppoAdmin(admin.StackedInline):
    model = Gruppo
    extra = 3

class GenericGroup(GroupAdmin):
    inlines = [GruppoAdmin, UserInLine]

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Borraccia, BorracciaAdmin)
admin.site.register(Invito, InvitoAdmin)
#admin.site.register(Utente, UtentAdmin)
admin.site.register(Sorso, SorsoAdmin)
admin.site.register(Vittorie, VittoriaAdmin)
admin.site.register(Group, GenericGroup)
admin.site.register(CodiceSconto, CodiceScontoAdmin)
