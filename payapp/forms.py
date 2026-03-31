from django import forms
from payapp.models import BalanceTransactions

class MakeTransactionForm(forms.ModelForm):

    class Meta:
        model = BalanceTransactions
        fields = ["payee_username", "recipient_username", "amount"]
        labels = {
            "payee_username": "payee (username)(!excluded!)",
            "recipient_username": "recipient (username)",
            "amount": "amount to send",
        }
        exclude = ["payee_username",]