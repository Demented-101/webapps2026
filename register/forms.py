from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import Balance

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        Balance.objects.create(name=instance, balance=500)
        return instance
