from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models
from payapp.forms import MakeTransactionForm
from django.db import transaction, OperationalError

@csrf_exempt
def home(request):
    user_balance = 0
    if request.user.is_authenticated: user_balance = models.Balance.objects.get(name__username=request.user.username).balance
    return render(request, "webapps2026/home.html", context={"user_balance":user_balance})

@csrf_protect
def make_transaction(request):
    if request.method == 'POST':
        form = MakeTransactionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:

            ## get all needed information
            form.payee_username = request.user.username
            src_username = request.user.username
            dst_username = form.cleaned_data["recipient_username"]
            amount_to_transfer = form.cleaned_data["amount"]

            ## get balance of both users
            try:
                src_balance = models.Balance.objects.select_related().get(name__username=src_username)
                dst_balance = models.Balance.objects.select_related().get(name__username=dst_username)
            except ObjectDoesNotExist:
                return render_form(request, form, error = "User does not exist")

            ## error checks to make sure numbers are valid
            if src_balance.balance < amount_to_transfer: return render_form(request, form, error = "Insufficient funds.")
            if amount_to_transfer <= 0: return render_form(request, form, error = "Invalid amount to send")

            ## run transaction atomically
            try:
                with transaction.atomic():
                    ## remove funds from user
                    src_balance.balance = src_balance.balance - amount_to_transfer
                    src_balance.save()
                    ## add funds to recipients account
                    dst_balance.balance = dst_balance.balance + amount_to_transfer
                    dst_balance.save()

            ## re-render form with transaction error
            except OperationalError:
                return render_form(request, form, error="Transaction Error")

            messages.info(request, "Transaction complete!")
        return redirect("/home")

    else: form = MakeTransactionForm()

    return render_form(request, form)

@csrf_exempt
def render_form(request, form, error = "N/a", info = "N/a"):
    if error != "N/a":
        messages.error(request, "Error: " + error)

    return render(request, "payapp/FundTransaction.html", {"form": form})