from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from payapp.forms import MakeTransactionForm, RequestTransactionForm
from django.db import transaction, OperationalError
from .models import BalanceTransaction, BalanceTransactionRequest
from register.models import BalanceUser
from administation.models import AdminUser


@csrf_exempt
def home(request):
    user_balance = 0
    has_unsent_request = False
    if request.user.is_authenticated:
        # get user balance
        user_balance = BalanceUser.objects.get(user__username=request.user.username).balance

        # has unsent transaction
        if len(get_open_requests(request.user.username)) > 0: has_unsent_request = True

    return render(request, "webapps2026/home.html", context={
        "user_balance":user_balance,
        "has_unsent_requests":has_unsent_request,
        "is_admin": is_admin(request),
    })

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
                src = BalanceUser.objects.get(user__username=src_username)
                src_balance = src.balance
                dst = BalanceUser.objects.get(user__username=dst_username)
                dst_balance = dst.balance
            except ObjectDoesNotExist:
                return render_form(request, form, "payapp/FundTransaction.html", error = "User does not exist")

            ## error checks to make sure numbers are valid
            if src.balance < amount_to_transfer: return render_form(request, form, "payapp/FundTransaction.html", error = "Insufficient funds.")
            if amount_to_transfer <= 0: return render_form(request, form, "payapp/FundTransaction.html", error = "Invalid amount to send")

            ## run transaction atomically
            try:
                with transaction.atomic():
                    ## remove funds from user
                    src.balance = src_balance - amount_to_transfer
                    src.save()
                    ## add funds to recipients account
                    dst.balance = dst_balance + amount_to_transfer
                    dst.save()

                    ## add transaction to database
                    BalanceTransaction.objects.create(
                        payee_username=src_username,
                        recipient_username=dst_username,
                        amount=amount_to_transfer,
                    ).save()

            ## re-render form with transaction error
            except OperationalError:
                return render_form(request,  form, "payapp/FundTransaction.html", error="Transaction Error")

            messages.info(request, "Transaction complete!")

        return redirect("/home")

    else: form = MakeTransactionForm()

    return render_form(request, form, "payapp/FundTransaction.html",)

@csrf_protect
def request_transaction(request):
    if request.method == "POST":
        form = RequestTransactionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:

            # get all needed information
            form.from_username = request.user.username
            src_username = request.user.username
            dst_username = form.cleaned_data["to_username"]
            amount_to_transfer = form.cleaned_data["amount"]

            # make sure the user exists
            if not BalanceUser.objects.filter(user__username=dst_username).exists() and dst_username != src_username:
                return render_form(request, form, "payapp/MakeTransactionRequest.html", error="User does not exist")

            # make sure number is valid
            if amount_to_transfer <= 0: return render_form(request, form, "payapp/MakeTransactionRequest.html", error="Invalid amount to send")

            # make request
            BalanceTransactionRequest(
                from_username=src_username,
                to_username=dst_username,
                amount=amount_to_transfer,
            ).save()
            messages.info(request, "Request Sent!")

        return redirect("/home")

    else: form = RequestTransactionForm()

    return render_form(request, form,"payapp/MakeTransactionRequest.html",)

@csrf_protect
def view_transactions(request):
    # get all transactions I am part of, and then sort them by newest to oldest
    username = request.user.username
    transactions = BalanceTransaction.objects.filter(recipient_username=username).values() | BalanceTransaction.objects.filter(payee_username=username).values()
    transactions = transactions.order_by("-created_at").values()

    return render(request, "payapp/Transactions.html", context={
        "transactions": transactions,
        "is_admin": is_admin(request),
    })

@csrf_protect
def view_transaction_requests(request, ignore_post=False):
    if request.method == "POST" and not ignore_post:
        if request.user.is_authenticated:
            # get request and response
            request_id = request.POST["id"]
            transaction_request = BalanceTransactionRequest.objects.get(id=request_id)
            dst_username = transaction_request.from_username # who should get paid in this interaction
            src_username = transaction_request.to_username # who is paying in this interaction
            amount_to_transfer = transaction_request.amount
            accepted = request.POST["response"] == "accept"

            if accepted: ## user accepted transaction
                ## get balance of both users
                try:
                    src = BalanceUser.objects.get(user__username=src_username)
                    dst = BalanceUser.objects.get(user__username=dst_username)

                    src_balance = src.balance
                    dst_balance = dst.balance

                except ObjectDoesNotExist: # user can be deleted after posting request
                    messages.error(request, "cannot load user balance")
                    return view_transaction_requests(request, True)

                ## run transaction atomically
                try:
                    with transaction.atomic():
                        ## remove funds from user
                        src.balance = src_balance - amount_to_transfer
                        src.save()
                        ## add funds to recipients account
                        dst.balance = dst_balance + amount_to_transfer
                        dst.save()

                        ## add transaction to database
                        BalanceTransaction.objects.create(
                            payee_username=src_username,
                            recipient_username=dst_username,
                            amount=amount_to_transfer,
                        ).save()

                        transaction_request.open = False
                        transaction_request.accepted = True
                        transaction_request.save()

                ## re-render form with transaction error
                except OperationalError:
                    messages.error(request, "Transaction error. Please try again.")
                    return view_transaction_requests(request, True)

                messages.info(request, "Transaction complete")

            else: ## user declines transaction
                transaction_request.open = False
                transaction_request.accepted = False
                transaction_request.save()
                messages.info(request, "Transaction declined")

        else: return redirect("/home")

    open_requests = []
    all_requests = []
    balance = 0
    if request.user.is_authenticated:
        username = request.user.username
        # get open requests that have not been responded to
        open_requests = get_open_requests(username)

        # get all requests sent or received
        set_a = BalanceTransactionRequest.objects.filter(to_username=username)
        set_b = BalanceTransactionRequest.objects.filter(from_username=username)
        all_requests = (set_a | set_b).order_by("-created_at").values()

        # get user balance
        balance = BalanceUser.objects.get(user__username=username).balance

    return render(request, "payapp/TransactionRequests.html", context={
        "open_requests":open_requests,
        "all_requests":all_requests,
        "balance":balance,
        "is_admin": is_admin(request),
    })

@csrf_exempt
def get_open_requests(username):
    transaction_requests = BalanceTransactionRequest.objects.filter(to_username=username) & \
                           BalanceTransactionRequest.objects.filter(open=True)
    return transaction_requests.values()

@csrf_exempt
def render_form(request, form, template_name, error = "N/a"):
    # add error message if needed
    if error != "N/a":
        messages.error(request, "Error: " + error)

    # return a render of the form.
    return render(request, template_name, {"form": form, "is_admin": is_admin(request)})

def is_admin(request):
    return AdminUser.objects.filter(user__username=request.user.username).exists()