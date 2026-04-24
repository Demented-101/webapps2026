from django.urls import path
from .views import get_conversion

my_url = "http://localhost:8000/conversion"

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<int:amount_of_currency1>', get_conversion),
]
