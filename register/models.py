from django.db import models
from django.contrib.auth.models import User

## user with balance and currency type
class BalanceUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField(default=500)
    currency_type = models.IntegerField(default=0)

    def __str__(self):
        details = ""
        details += f"username: {self.user.username}\n"
        details += f"full name: {self.user.first_name} {self.user.last_name}\n"
        details += f"balance: {self.balance}\n"
        return details
