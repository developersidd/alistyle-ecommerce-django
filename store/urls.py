from django.urls import include, path
from . import views

urlpatterns = [
    # path("store/", views.store_home),
    path("submit_review/<int:product_id>/", views.submit_review, name="submit_review"),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    # path("<slug:category_slug>/", views.products_by_category, name="products_by_category"),
]
