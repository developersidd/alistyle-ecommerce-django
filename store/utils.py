from datetime import timedelta
from django.db import models
from django.utils import timezone
from store.models import Product, ProductView


def track_product_view(request, product):
    """
    Track a product view for analytics and user behavior analysis.
    """
    # get or create session key
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # check if the product has already been viewed in this session
    recent_view = ProductView.objects.filter(
        session_key=session_key,
        product=product,
        viewed_at__gte=timezone.now() - timedelta(minutes=30),
    ).exists()

    if not recent_view:
        # create a new product view record
        ProductView.objects.create(
            session_key=session_key,
            product=product,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        )

        # Increment product view count
        Product.objects.filter(pk=product.pk).update(
            view_count=models.F("view_count") + 1, last_viewed=timezone.now()
        )

        return True
    return False


def get_client_ip(request):
    """
    Retrieve the client's IP address from the request.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
