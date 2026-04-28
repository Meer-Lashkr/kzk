from django.contrib import admin
from .models import ValidationItem, ValidationVote


@admin.register(ValidationItem)
class ValidationItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data_type",
        "status",
        "yes_votes",
        "no_votes",
        "total_votes",
        "confidence_score",
        "validated_by",
        "created_at",
    )
    list_filter = ("data_type", "status", "validated_by")
    search_fields = ("content",)
    readonly_fields = (
        "yes_votes",
        "no_votes",
        "total_votes",
        "confidence_score",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(ValidationVote)
class ValidationVoteAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user", "response", "created_at")
    list_filter = ("response",)
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
