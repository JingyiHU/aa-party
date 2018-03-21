from django.contrib import admin
from .models import Party, Contacter, House


class ContacterAdmin(admin.ModelAdmin):
    model = Contacter
    list_display = ['verbose_name', 'email']


class HouseAdmin(admin.ModelAdmin):
    model = House
    list_display = ['house_info']


admin.site.register(Party)
admin.site.register(Contacter, ContacterAdmin)
admin.site.register(House, HouseAdmin)