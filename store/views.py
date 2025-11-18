from math import prod
from django.contrib import messages
from django.shortcuts import redirect, render

from store.forms import ReviewForm
from store.models import Product, ProductGallery, ReviewRating


# store view
def store(request, category_slug=None, flash_sale=None):
    if category_slug:
        products = (
            Product.objects.filter(
                category__slug=category_slug, is_available=True, is_active=True
            )
            .order_by("id")
        )
    elif flash_sale:
        products = (
            Product.objects.filter(
                flash_sales__id=flash_sale, is_available=True, is_active=True
            )
            .order_by("id")
        )
    products = (
        Product.objects.all().filter(is_available=True, is_active=True).order_by("id")
    )
    context = {"products": products}
    return render(request, "store/store.html", context=context)


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


# Submit a product review
def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("store")

    if request.method == "POST":
        current_user = request.user
        try:
            review = ReviewRating.objects.get(
                user__id=current_user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your review has been updated.")
                return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = ReviewRating()
                data = form.cleaned_data
                review.rating = data["rating"]
                review.review = data["review"]
                review.subject = data["subject"]
                review.user = current_user
                review.product = product
                review.ip = request.META.get("REMOTE_ADDR")
                review.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
