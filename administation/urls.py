from django.urls import path, include
from . import views

urlpatterns = [
    path("ViewUsers", views.view_users, name="Users"),
    path("ViewTransactions", views.view_transactions, name="Transactions"),
    path("ViewTransactionRequests", views.view_transaction_requests, name="TransactionRequests"),
]