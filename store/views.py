from django.contrib import messages
from django.shortcuts import redirect, render

from store.forms import ReviewForm
from store.models import Product, ProductGallery, ReviewRating, Variation


# store view
def store(request, category_slug=None):
    category_slugs = request.GET.getlist("category_slug") or None
    sizes = request.GET.getlist("size") or None
    min_price = request.GET.get("min_price", "0")
    max_price = request.GET.get("max_price", "100000")
    layout = request.GET.get("layout", "grid")
    sort_by = request.GET.get("sort_by", "latest_items")
    try:
        min_price_int = int(min_price)
        max_price_int = int(max_price)
    except ValueError:
        min_price_int = 0
        max_price_int = 100000

    products = Product.objects.filter(is_available=True, is_active=True)
    # Apply category filter
    if category_slugs and len(category_slugs) > 0:
        products = products.filter(
            category__slug__in=category_slugs,
        )
    # Apply single category filter
    elif category_slug:
        products = products.filter(category__slug=category_slug)

    # Apply price filter
    products = products.filter(price__gte=min_price_int, price__lte=max_price_int)

    # Apply size filter
    if sizes and len(sizes) > 0:
        products = products.filter(
            variations__variation_category="size",
            variations__variation_value__in=sizes,
        ).distinct()

    # Get available sizes from variations
    available_sizes = (
        Variation.objects.filter(variation_category="size")
        .values_list(
            "variation_value", flat=True
        )  # value_list to get a flat list of size values
        .distinct()
        .order_by("variation_value")
    )

    #query_dict = request.GET.copy()
    #query_dict.pop("layout", None)
    #query_string_without_layout = query_dict.urlencode()

    context = {
        "products": products,
        "available_sizes": available_sizes,
        "category_slugs": category_slugs,
        "selected_sizes": sizes,
        "min_price": min_price,
        "max_price": max_price,
    }
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
