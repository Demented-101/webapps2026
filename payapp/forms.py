from django import forms
from payapp.models import BalanceTransaction, BalanceTransactionRequest

class MakeTransactionForm(forms.ModelForm):

    class Meta:
        model = BalanceTransaction
        fields = ["payee_username", "recipient_username", "amount"]
        labels = {
            "payee_username": "payee (username)(!excluded!)",
            "recipient_username": "recipient (username)",
            "amount": "amount to send",
        }
        exclude = ["payee_username",]

class RequestTransactionForm(forms.ModelForm):

    class Meta:
        model = BalanceTransactionRequest
        fields = ["from_username", "to_username", "amount"]
        labels = {
            "from_username": "sent by (username)(!excluded!)",
            "to_username": "Send to (username)",
            "amount": "Requested amount",
        }
        exclude = ["from_username"]
