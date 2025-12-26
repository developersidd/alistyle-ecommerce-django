from django.db import models
from .models import Category


def menu_links(request):
    links = Category.objects.annotate(
        product_count=models.Count(
            "products", filter=models.Q(products__is_active=True)
        )
    )
    return dict(category_links=links)
