from django.urls import include, path
from . import views

urlpatterns = [
    # path("store/", views.store_home),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    # path("<slug:category_slug>/", views.products_by_category, name="products_by_category"),
]
