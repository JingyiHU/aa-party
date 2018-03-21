import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from geoposition.fields import GeopositionField
from djmoney.models.fields import MoneyField


class Contacter(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_("first_name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last_name"), max_length=100)
    email = models.EmailField(verbose_name=_("email"), null=False)
    phone_number = PhoneNumberField(verbose_name=_("phone_number"), null=True, blank=True)

    def verbose_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class House(models.Model):
    house_name = models.CharField(verbose_name=_("house_name"), max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name=_("address"), max_length=256, null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    owner = models.ForeignKey("Contacter", null=True, blank=True, on_delete=models.CASCADE)
    electric_fee = MoneyField(verbose_name=_("electric_fee"), max_digits=10, decimal_places=2, default_currency='EUR')
    water_fee = MoneyField(verbose_name=_("water_fee"), max_digits=10, decimal_places=2, default_currency='EUR')

    def house_info(self):
        return self.house_name + "(" + str(self.owner if self.owner else " ") + ")"

    def __str__(self):
        return self.house_name


class Party(models.Model):
    PARTY_STATUS = (
        ('NOTBEGIN', _('Not begin')),
        ('RUNNING', _('Running')),
        ('ENDED', _('Ended')),
        ('OTHER', _('Other status')),
    )

    name = models.CharField(verbose_name=_("party_name"), max_length=256, blank=True, null=False)
    creator = models.ForeignKey("Contacter", on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(verbose_name=_("party_time"), default=datetime.datetime.now)
    duration = models.TimeField(verbose_name=_("duration"), null=True)
    participation = models.ManyToManyField("Contacter", related_name=_('participation'))
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True)
    chef = models.ManyToManyField("Contacter", related_name=_('chef'))
    cleaner = models.ManyToManyField("Contacter", related_name=_('cleaner'))
    status = models.CharField(null=False, choices=PARTY_STATUS, max_length=100, default="OTHER")

