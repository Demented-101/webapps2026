from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import requests
from django.urls import resolve
from django.http import HttpRequest
from django.template.defaulttags import url

from .models import BalanceUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency_type = forms.ChoiceField(required=True, choices=[('GDP','GDP'), ('USD', 'USD'), ('EUR', 'EUR')])

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "currency_type", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)

        currency_type = self.cleaned_data["currency_type"]
        api_url = resolve("/conversion/GBP/" + currency_type + "/500").url_name

        print(api_url)
        print(currency_type)

        if api_url is not None:
            balance = requests.get(api_url, params="GET")
        else:
            balance = 500

        BalanceUser.objects.create(user=instance, balance=balance, currency_type=currency_type).save()
        return instance
