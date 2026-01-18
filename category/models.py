from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(
        max_length=50, blank=True, default="This is category"
    )
    cat_img = CloudinaryField("cat_img", folder="django-ecommerce")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse("products_by_category", args=[self.slug])
