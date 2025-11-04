from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "username",
        "last_login",
        "is_active",
        "date_joined",
    )

    list_display_links = ("email", "first_name", "last_name")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account)
