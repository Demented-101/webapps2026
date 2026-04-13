from django.db import models
from django.contrib.auth.models import User

# class Balance(models.Model):
#     name = models.ForeignKey(User, on_delete=models.CASCADE)
#     balance = models.IntegerField(default=500)
#
#     def __str__(self):
#         details = ""
#         details += f"Username       : {self.name}\n"
#         details += f"Acc balance    : {self.balance}\n"
#         return details

class BalanceTransactionRequest(models.Model):
    from_username = models.CharField(max_length=150)
    to_username = models.CharField(max_length=150)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        details = ""
        details += f"From (Username)    : {self.from_username}\n"
        details += f"To (Username)      : {self.to_username}\n"
        details += f"Amount sent        : {self.amount} (in default currency)\n"
        details += f"Date sent          : {self.created_at}\n"
        details += f"Open               : {self.open}\n"
        if self.open: return details
        details += f"accepted           : {self.accepted}\n"
        return details

class BalanceTransaction(models.Model):
    payee_username = models.CharField(max_length=150)
    recipient_username = models.CharField(max_length=150)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        details = ""
        details += f"From (Username)    : {self.payee_username}\n"
        details += f"To (Username)      : {self.recipient_username}\n"
        details += f"Amount sent        : {self.amount} (in default currency)\n"
        details += f"Date sent          : {self.created_at}\n"
        return details
