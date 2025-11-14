import admin_thumbnails
from django.contrib import admin

from store.models import (
    BannerSlider,
    Campaign,
    FlashSale,
    Product,
    ProductGallery,
    ReviewRating,
    Variation,
)


# Register your models here.
@admin_thumbnails.thumbnail("image")
class ProductImageInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ReviewInline(admin.TabularInline):
    model = ReviewRating
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product_name",
        "category",
        "price",
        "final_price",
        "stock",
        "is_available",
        "updated_at",
        "created_at",
    )

    list_display_links = ("product_name",)
    search_fields = ("product_name",)
    prepopulated_fields = {"slug": ("product_name",)}
    inlines = [ProductImageInline, ReviewInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product",
        "variation_category",
        "variation_value",
        "is_active",
    )
    list_editable = ("is_active",)
    list_display_links = ("product",)
    list_filter = ("product", "variation_category", "variation_value")


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "discount_percent",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )
    filter_horizontal = ("categories", "products")
    list_filter = ("start_date", "end_date")


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = (
        # "products",
        # "categories",
        "discount_percent",
        "start_time",
        "end_time",
        "is_active",
        "created_at",
    )
    filter_horizontal = ("categories", "products")
    list_filter = ("start_time", "end_time")


@admin.register(BannerSlider)
class BannerSliderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "position",
        "is_active",
        "created_at",
    )


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "review",
        "status",
        "created_at",
        "updated_at",
    )
    list_editable = ("status", "rating")
    list_filter = ("status", "created_at", "updated_at")


admin.site.register(ProductGallery)
