from math import prod
from django.shortcuts import render

from store.models import Product, ProductGallery, ReviewRating


# Product detail view
def product_detail(request, category_slug, product_slug):

    try:
        product = Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e
    
    # TODO: check if the product is in cart also check order status
    
    # Reviews
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    # Photos
    product_photos = ProductGallery.objects.filter(product_id=product.id)
    
    # context
    context = {"product": product, "reviews": reviews, "product_photos": product_photos}
    return render(request, "store/product_detail.html", context=context)
