from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from administation.models import AdminUser
from register.models import BalanceUser
from payapp.models import *
from django.core.exceptions import ObjectDoesNotExist
from payapp.views import is_admin
from django.contrib import messages
from django.db import transaction, OperationalError

@csrf_protect
def admin_homepage(request):
    return render(request, "Administration/home.html", {
        "registered_by": AdminUser.objects.get(user__username=request.user.username).registered_by,
        "is_admin": is_admin(request),
    })

@csrf_protect
def view_users(request):
    return render(request, "Administration/Users.html", {
        "users": BalanceUser.objects.all(),
        "admins": AdminUser.objects.all(),
        "is_admin": is_admin(request),
    })

@csrf_protect
def view_transactions(request):
    return render(request, "Administration/Transactions.html", {
        "transactions": BalanceTransaction.objects.all().order_by("-created_at"),
        "is_admin": is_admin(request),
    })

@csrf_protect
def view_transaction_requests(request):
    return render(request, "Administration/TransactionRequests.html", {
        "transaction_requests": BalanceTransactionRequest.objects.all().order_by("-created_at"),
        "is_admin": is_admin(request),
    })

@csrf_protect
def register_new_admin(request):
    if request.method == "POST":
        if request.user.is_authenticated and is_admin(request):
            # get targeted username
            target_username = request.POST["target_username"]
            try:
                target_user = User.objects.get(username=target_username)
            except ObjectDoesNotExist:
                messages.error(request, "could not find user with this username")
                return render(request, "Administration/RegisterAdmin.html", {"is_admin": is_admin(request)})

            if AdminUser.objects.filter(user__username=target_username).exists():
                messages.info(request, "this user is already an admin")
                return render(request, "Administration/RegisterAdmin.html", {"is_admin": is_admin(request)})

            ## run transaction atomically
            try:
                with transaction.atomic():
                    AdminUser.objects.create(user=target_user, registered_by=request.user)
            except OperationalError:
                messages.error(request, "could not register user as admin.")
                return render(request, "Administration/RegisterAdmin.html", {"is_admin": is_admin(request)})

            messages.info(request, "user registered as admin successfully")
            return redirect("/home")

        else: ## not valid user (admin/logged in)
            messages.error(request, "invalid credentials")
            return redirect("/home")

    return render(request, "Administration/RegisterAdmin.html", {"is_admin": is_admin(request)})
