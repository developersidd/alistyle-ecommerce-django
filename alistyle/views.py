from datetime import datetime
from django.shortcuts import render
from django.utils import timezone

from store.models import Campaign, FlashSale, Product


def home(request):
    now = datetime.now()
    start_time = None
    end_time = None
    # Flash Sale Products (only active)
    flash_sale = (
        FlashSale.objects.filter(start_time__lte=now, end_time__gte=now, is_active=True)
        .prefetch_related("categories")
        .order_by("start_time")
        .first()
    )
    flash_sale_categories = []
    if flash_sale:
        start_time = flash_sale.start_time
        end_time = flash_sale.end_time
        for category in flash_sale.categories.all():
            data = {
                "category": category,
                "discount_percent": flash_sale.discount_percent,
            }
            flash_sale_categories.append(data)
    # get popular products
    popular_products = Product.objects.filter(is_active=True).order_by(
        "-view_count", "-purchase_count", "-cart_add_count"
    )[:8]

    # newly arrived products
    new_arrivals = Product.objects.filter(is_active=True).order_by("-created_at")[:8]

    # Active Campaigns
    #    active_campaigns = Campaign.objects.filter(
    #        start_date__lte=today, end_date__gte=today
    #    ).prefetch_related("products", "categories")
    #
    #    # Get products that have product-level discount
    #    discounted_products = Product.objects.filter(
    #        discount_percent__gt=0, discount_start__lte=today, discount_end__gte=today
    #    )
    #
    context = {
        "flash_sale": (
            {
                "categories": flash_sale_categories,
                "start_time": start_time,
                "end_time": end_time,
            }
            if flash_sale
            else None
        ),
        "popular_products": popular_products,
        "new_arrivals": new_arrivals,
        # "campaigns": active_campaigns,
        # "discounted_products": discounted_products,
    }

    return render(request, "home.html", context)
