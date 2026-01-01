from django.forms import ModelForm

from orders.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "address_line_1",
            "address_line_2",
            "state",
            "city",
            "order_note",
        ]
