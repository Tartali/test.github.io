#models.py
from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Choose(models.Model):
    count_black = models.PositiveIntegerField(default=0, verbose_name="black")
    count_white = models.PositiveIntegerField(default=0, verbose_name="white")
    count_purple = models.PositiveIntegerField(default=0, verbose_name="purple")
    voter = models.ForeignKey(User, null=True, blank=True, verbose_name='Пользователь', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.voter.username})


class Comment(models.Model):
    title = models.CharField(max_length=30, default="tit")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def get_absolute_url(self):
        return reverse("comment")


class UsernameMaxAdapter(DefaultAccountAdapter):

    def clean_username(self, username, **kwargs):
        if len(username) > 20:
            raise ValidationError('Please enter a username value less than the current one')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.