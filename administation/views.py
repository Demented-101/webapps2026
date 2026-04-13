from django.shortcuts import render
from register.models import BalanceUser
from payapp.models import *
from payapp.views import is_admin

def view_users(request):
    return render(request, "Administration/Users.html", {
        "users": BalanceUser.objects.all(),
        "is_admin": is_admin(request),
    })

def view_transactions(request):
    return render(request, "Administration/Transactions.html", {
        "transactions": BalanceTransaction.objects.all(),
        "is_admin": is_admin(request),
    })

def view_transaction_requests(request):
    return render(request, "Administration/TransactionRequests.html", {
        "transaction_requests": BalanceTransactionRequest.objects.all(),
        "is_admin": is_admin(request),
    })