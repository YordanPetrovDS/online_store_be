from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from geo.models import Country, State


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True, blank=True, verbose_name=_("username"))
    email = models.EmailField(max_length=64, unique=True, verbose_name=_("email"))
    first_name = models.CharField(max_length=32, blank=True, verbose_name=_("first name"))
    last_name = models.CharField(max_length=32, blank=True, verbose_name=_("last name"))
    phone = models.CharField(max_length=32, blank=True, verbose_name=_("phone"))
    is_email_confirmed = models.BooleanField(default=False, verbose_name=_("is email confirmed"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("deleted at"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def full_name(self) -> str:
        return " ".join(filter(None, [self.first_name, self.last_name]))

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("user"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("bio"))
    location = models.CharField(max_length=30, blank=True, verbose_name=_("location"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user.full_name} profile"


class UserAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("user"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("country"))
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, blank=True, related_name="addresses", verbose_name=_("state")
    )
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=256, verbose_name=_("address"))
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("user address")
        verbose_name_plural = _("user addresses")

    def __str__(self):
        return f"{self.country}, {self.city}, {self.address}"


class UserWishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists", verbose_name=_("user"))
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.CASCADE, related_name="wishlists", verbose_name=_("product")
    )
    has_notifications = models.BooleanField(default=True, verbose_name=_("has notifications"))

    class Meta:
        verbose_name = _("user wishlist")
        verbose_name_plural = _("user wishlists")
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_user_product_wishlist")]

    def __str__(self):
        return f"{self.user.full_name} - {self.product.sku}"


class UserReview(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("user"))
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.CASCADE, related_name="reviews", verbose_name=_("product")
    )
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_("rate"))
    review = models.TextField(verbose_name=_("review"))
    is_approved = models.BooleanField(default=False, verbose_name=_("is approved"))

    class Meta:
        verbose_name = _("user review")
        verbose_name_plural = _("user reviews")

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.sku}"
