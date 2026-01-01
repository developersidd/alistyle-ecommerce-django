from django.shortcuts import render

# Create your views here.
def ssl_payment(request):
    order_number = request.POST["order_number"]
    name = request.POST["full_name"]
    amount_to_pay = request.POST["grand_amount"] 
    pass