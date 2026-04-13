from django.contrib import admin
from .models import *

class BalanceTransAdmin(admin.ModelAdmin):
    list_display = ["payee_username", "recipient_username", "amount", "created_at"]
admin.site.register(BalanceTransaction, BalanceTransAdmin)

class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = ["from_username", "to_username", "amount", "created_at", "open", "accepted"]
admin.site.register(BalanceTransactionRequest, TransactionRequestAdmin)

