from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import requests
from conversion.urls import my_url as base_url

from .models import BalanceUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency_type = forms.ChoiceField(required=True, choices=[('GBP','GBP'), ('USD', 'USD'), ('EUR', 'EUR')])

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "currency_type", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)

        currency_type = self.cleaned_data["currency_type"]
        balance = requests.get(base_url + f'/GBP/{currency_type}/500').headers["Converted_amount"]
        BalanceUser.objects.create(user=instance, balance=int(float(balance)), currency_type=currency_type).save()

        return instance
