#models.py
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from payments import PurchasedItem
from payments.models import BasePayment


class Choose(models.Model):
    count_black = models.PositiveIntegerField(default=0, verbose_name="black")
    count_white = models.PositiveIntegerField(default=0, verbose_name="white")
    count_purple = models.PositiveIntegerField(default=0, verbose_name="purple")
    voter = models.ForeignKey(User, null=True, blank=True, verbose_name='Пользователь', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.voter.username})


class Comment(models.Model):
    title = models.CharField(max_length=30, default="tit")

    def get_absolute_url(self):
        return reverse("comment")


class Payment(BasePayment):
    def get_failure_url(self):
        return 'http://example.com/failure/'

    def get_success_url(self):
        return 'http://example.com/success/'

    def get_purchased_items(self):
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV', quantity=9, price=Decimal(1), currency='USD')