from django.contrib.auth.models import User
from django.db import models

class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered_by = models.CharField(max_length=150)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        details = ""
        details += f"user:( {self.user} )\n"
        details += f"registered_by: {self.registered_by}\n"
        details += f"registered_on: {self.registered_on}\n"
        return details

