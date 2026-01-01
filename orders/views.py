import math
from django.contrib import messages
from django.shortcuts import redirect, render

from carts.utils import get_cart_items, get_or_create_cart
from coupon.models import CouponUsage
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.


def place_order(request, total=0):
    cart = get_or_create_cart(request)
    cart_items = get_cart_items(request.user, cart)
    coupon_discount = 0
    tax = 0
    order = None
    grand_total = 0
    coupon_usage_id = request.session.get("coupon_usage_id")
    current_user = request.user
    for item in cart_items:
        total += item.product.final_price() + item.quantity
    tax = math.ceil(2 * total) / 100
    grand_total = total + tax
    if coupon_usage_id:
        coupon_usage = (
            CouponUsage.objects.filter(user=current_user, id=coupon_usage_id)
            .order_by("-used_at")
            .first()
        )
        # Apply discount to grand total
        if coupon_usage and total > coupon_usage.discount_amount:
            coupon_discount = int(coupon_usage.discount_amount)
            grand_total -= coupon_discount

    if request.method == "POST":
        print("Order form submitted")
        try:
            orderForm = OrderForm(request.POST)
            if orderForm.is_valid():
                cleaned_data = orderForm.cleaned_data
                order = Order()
                order.user = current_user
                order.first_name = cleaned_data["first_name"]
                order.last_name = cleaned_data["last_name"]
                order.email = cleaned_data["email"]
                order.phone_number = cleaned_data["phone_number"]
                order.city = cleaned_data["city"]
                order.state = cleaned_data["state"]
                order.address_line_1 = cleaned_data["address_line_1"]
                order.address_line_1 = cleaned_data["address_line_1"]
                order.order_note = cleaned_data["order_note"]
                order.tax = tax
                order.order_total = grand_total
                order.save()
            else:
                messages.error(request, "There was error an occurred")
                return redirect("checkout")

        except Exception as e:
            messages.error(request, "There was error an occurred")
            return redirect("checkout")

    return render(
        request,
        "order/place_order.html",
        {
            "order": order,
            "total": total,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
            "discount": coupon_discount,
        },
    )
