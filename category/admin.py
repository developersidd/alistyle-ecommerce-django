from django.contrib import admin

from category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "category_name",
        "slug",
        "get_product_count",
    )
    search_fields = ("category_name",)
    prepopulated_fields = {"slug": ("category_name",)}

    def get_product_count(self, obj):
        return obj.products.count()

    get_product_count.short_description = "Number of Products"


admin.site.register(Category, CategoryAdmin)
