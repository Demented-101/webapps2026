from django.http import HttpResponse, Http404

GBP_CONVERSIONS = {
    'GBP': 1,
    'EUR': 1.15,
    'USD': 1.35,
}
EUR_CONVERSIONS = {
    'GBP': 0.87,
    'EUR': 1,
    'USD': 1.17,
}
USD_CONVERSIONS = {
    'GBP': 0.74,
    'EUR': 0.85,
    'USD': 1,
}
CURRENCIES = {
    'GBP': GBP_CONVERSIONS,
    'EUR': EUR_CONVERSIONS,
    'USD': USD_CONVERSIONS,
}

def get_conversion(request, currency1, currency2, amount_of_currency1):
    ## verify URL is valid
    if not currency1 in CURRENCIES.keys(): raise Http404
    if not currency2 in CURRENCIES.keys(): raise Http404

    ## make conversion
    conversion = CURRENCIES[currency1][currency2]
    converted_amount = conversion * amount_of_currency1

    ## return response
    return HttpResponse(headers={'Conversion':conversion, 'Converted_amount':converted_amount})
