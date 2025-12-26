from modeltranslation.translator import translator, TranslationOptions
from store.models import Product, Category, ReviewRating


class ProductTranslationOptions(TranslationOptions):
    fields = ("product_name", "description")


translator.register(Product, ProductTranslationOptions)
