from django.contrib import admin
from unfold.admin import ModelAdmin

from newsletter.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ("email", "is_email_confirmed")
    list_filter = ("is_email_confirmed",)
    search_fields = ("email",)
