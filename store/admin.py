from datetime import date
import admin_thumbnails
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from store.models import (
    BannerSlider,
    Campaign,
    FlashSale,
    FlashSaleCategory,
    FlashSaleProduct,
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
        "price",
        "get_active_discount",
        "get_final_price",
        "category",
        "stock",
        "is_available",
        "created_at",
    )
    list_filter = ("is_available", "category", "created_at")
    list_editable = ("price", "stock", "is_available")
    list_display_links = ("product_name",)
    search_fields = ("product_name", "slug")
    prepopulated_fields = {"slug": ("product_name",)}
    inlines = [ProductImageInline, ReviewInline]

    def get_active_discount(self, obj):
        discount_info = obj.get_active_discount_info()
        if discount_info:
            color_map = {
                "campaign": "#17a2b8",  # Info color
                "flash_sale": "#ffc107",  # Warning color
                "product_discount": "#28a745",  # Success color
            }
            color = color_map.get(discount_info["type"], "#6c757d")  # Default gray
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">-{}%</span>',
                color,
                discount_info["percent"],
            )
        return format_html('<span style="color: #6c757d;">No discount</span>')

    get_active_discount.short_description = "Active Discount"

    def get_final_price(self, obj):
        final = obj.final_price()
        if final < obj.price:
            return format_html(
                '<strong style="color: #28a745;">${}</strong> <del style="color: #6c757d;">${}</del>',
                final,
                obj.price,
            )
        return f"${obj.price}"

    get_final_price.short_description = "Price"

    class Meta:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


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
        "get_status",
        "get_item_count",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )
    filter_horizontal = ("categories", "products")
    list_filter = ("is_active", "start_date", "end_date", "discount_percent")
    search_fields = ("title",)
    date_hierarchy = "start_date"  # To navigate campaigns by start date
    fieldsets = (
        ("Basic Information", {"fields": ("title", "discount_percent", "is_active")}),
        ("Schedule", {"fields": ("start_date", "end_date")}),
        (
            "Apply To",
            {
                "fields": ("categories", "products"),
                "description": "Select categories and products to which this campaign applies.",
            },
        ),
    )

    def get_status(self, obj):
        today = date.today()
        if obj.is_active and obj.start_date <= today <= obj.end_date:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">● ACTIVE</span>'
            )
        elif obj.start_date > today:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">⏱ UPCOMING</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">✓ EXPIRED</span>'
            )

    get_status.short_description = "Status"

    def get_item_count(self, obj):
        category_count = obj.categories.count()
        product_count = obj.products.count()
        return format_html(
            "<span style='color: #007bff;'>{} Products {} Categories</span>",
            product_count,
            category_count,
        )

    get_item_count.short_description = "Items"


class FlashSaleCategoryInline(admin.TabularInline):
    model = FlashSaleCategory
    extra = 2
    fields = ("category", "discount_percent", "get_product_count")
    readonly_fields = ("get_product_count",)
    autocomplete_fields = ("category",)  # To enable search in the foreign key field

    def get_product_count(self, obj):
        if obj.category:
            count = obj.category.products.count()
            return format_html("<span style='color: #007bff;'>{}</span>", count)
        return "-"

    get_product_count.short_description = "Number of Products"


class FlashSaleProductInline(admin.TabularInline):
    model = FlashSaleProduct
    extra = 2
    fields = ("product", "discount_percent", "get_original_price", "get_final_price")
    readonly_fields = ("get_original_price", "get_final_price")
    autocomplete_fields = ("product",)

    def get_original_price(self, obj):
        if obj.product:
            return f"৳{obj.product.price}"
        return "-"

    def get_final_price(self, obj):
        if obj.product:
            discounted_price = obj.product.price * (1 - obj.discount_percent / 100)
            return format_html(
                "<span style='color: #28a745;'>৳{:.2f}</span>", discounted_price
            )
        return "-"

    get_original_price.short_description = "Original Price"
    get_final_price.short_description = "Final Price"


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_status",
        "start_time",
        "end_time",
        "get_item_count",
        "is_active",
        "created_at",
    )
    list_filter = ("start_time", "end_time", "is_active")
    search_fields = ("title",)
    date_hierarchy = "start_time"
    inlines = [FlashSaleCategoryInline, FlashSaleProductInline]
    fieldsets = (
        ("Basic Information", {"fields": ("title", "is_active")}),
        (
            "Schedule",
            {
                "fields": ("start_time", "end_time"),
                "description": "Set the start and end time for the flash sale.",
            },
        ),
    )

    def get_status(self, obj):
        now = timezone.now()
        if obj.is_active and obj.start_time <= now <= obj.end_time:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">● LIVE</span>'
            )
        elif obj.start_time > now:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">⏱ SCHEDULED</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">✓ ENDED</span>'
            )

    get_status.short_description = "Status"

    def get_item_count(self, obj):
        category_count = obj.flash_sale_categories.count()
        product_count = obj.flash_sale_products.count()
        return format_html(
            "<span style='color: #007bff;'>{} Products {} Categories</span>",
            product_count,
            category_count,
        )

    get_item_count.short_description = "Items"


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
