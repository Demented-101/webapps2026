from django.db import models
from django.contrib.auth.models import User

class Balance(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=500)

    def __str__(self):
        details = ""
        details += f"Username       : {self.name}\n"
        details += f"Acc balance    : {self.balance}\n"
        return details

class BalanceTransactions(models.Model):
    payee_username = models.CharField(max_length=150)
    recipient_username = models.CharField(max_length=150)
    amount = models.IntegerField()

    def __str__(self):
        details = ""
        details += f"From (Username)    : {self.payee_username}\n"
        details += f"To (Username)      : {self.recipient_username}\n"
        details += f"Amount sent        : {self.amount} (in default currency)\n"
        return details
