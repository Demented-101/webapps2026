from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BalanceUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        BalanceUser.objects.create(user=instance, balance=500).save()
        return instance
