from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.view_transactions, name="transactions"),
    path("transactions", views.view_transactions, name="transactions"),
    path("makeTransaction", views.make_transaction, name="make transaction"),
    path("requestTransaction", views.request_transaction, name="request transaction"),
    path("TransactionRequests", views.view_transaction_requests, name="transaction requests"),

]