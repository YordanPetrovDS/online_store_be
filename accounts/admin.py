from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from accounts.models import Profile, User, UserAddress, UserReview, UserWishlist


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_email_confirmed",
        "created_at",
        "deleted_at",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_email_confirmed")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            ("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "is_email_confirmed", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "last_name", "phone", "password1", "password2"),
            },
        ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    list_display = ("user", "country", "state", "city", "address", "is_default")
    list_filter = ("country", "state", "city", "is_default")
    search_fields = ("user__username", "user__email", "city", "address")
    ordering = ("user", "country", "city")
    fieldsets = ((None, {"fields": ("user", "country", "state", "city", "address", "is_default")}),)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ["user", "bio", "location", "birth_date"]


@admin.register(UserWishlist)
class UserWishlistAdmin(ModelAdmin):
    list_display = ["user", "product", "has_notifications"]
    unique_together = ("user", "product")


@admin.register(UserReview)
class UserReviewAdmin(ModelAdmin):
    list_display = ("user", "product", "rate", "is_approved")
    list_filter = ("is_approved", "rate", "product__brand")
    search_fields = ("user__username", "product__sku", "review")
